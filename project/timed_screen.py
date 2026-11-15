"""Deadline-aware curses screen adapter for Titanic Escape.

The adapter preserves existing puzzle calls (addstr, getstr, refresh, etc.)
while enforcing room deadlines during interactive input.
"""
import curses
import math
import time

class RoomTimeExpired(Exception):
    """Raised when the active room runs out of time."""

class TimedScreen:
    POLL_MS = 100

    def __init__(self, screen, allowed_seconds, clock=time.monotonic, room_name=None, room_number=None, total_rooms=6):
        self._screen = screen
        self._clock = clock
        self.allowed_seconds = max(0.0, float(allowed_seconds))
        self.deadline = clock() + self.allowed_seconds
        self.room_name = room_name
        self.room_number = room_number
        self.total_rooms = total_rooms

    def __getattr__(self, name):
        return getattr(self._screen, name)

    def remaining_seconds(self):
        return max(0.0, self.deadline - self._clock())

    def flood_fraction(self):
        """Calculate how much of the room's time has elapsed."""
        if self.allowed_seconds <= 0:
            return 1.0
        return max(0.0, min(1.0, 1.0 - self.remaining_seconds() / self.allowed_seconds)
        )

    def _flood_meter(self, width=12):
        """Create an ASCII flooding progress bar."""
        filled = min(width, int(self.flood_fraction() * width))

        return (
            f"FLOOD [{'~' * filled}{'.' * (width - filled)}] "
            f"{self.flood_fraction():.0%}"
        )

    def check_deadline(self):
        if self._clock() >= self.deadline:
            raise RoomTimeExpired

    def _draw_header(self):
        """A compact 3-row HUD, compatible with puzzles beginning at row 3+."""
        if not self.room_name or self.room_number is None:
            return
        height, width = self._screen.getmaxyx()
        if height < 3 or width < 40:
            return

        usable = width - 1
        title = f" TITANIC ESCAPE  |  ROOM {self.room_number}/{self.total_rooms} "
        location = f" LOCATION: {self.room_name} "
        completed = max(0, min(self.room_number - 1, self.total_rooms))
        slots = ''.join('[#]' if i < completed else '[ ]' for i in range(self.total_rooms))
        progress = f" PROGRESS: {slots} "
        try:
            self._screen.addstr(0, 0, title[:usable].ljust(usable), curses.A_BOLD)
            self._screen.addstr(1, 0, location[:usable].ljust(usable))
            self._screen.addstr(2, 0, progress[:usable].ljust(usable))

            meter = self._flood_meter()
            meter_col = usable - len(meter)

            if meter_col > len(progress):
                water_style = (
                    curses.A_BOLD
                    if self.flood_fraction() >= 0.75
                    else curses.A_NORMAL
                )

                self._screen.addstr(2, meter_col, meter, water_style)
        except curses.error:
            pass

    def _draw_clock(self):
        self.check_deadline()
        height, width = self._screen.getmaxyx()
        if height < 1 or width < 18:
            return
        seconds = math.ceil(self.remaining_seconds())
        label = f"TIME {seconds}"
        col = width - len(label) - 2
        try:
            attr = curses.A_BOLD
            if seconds <= 10 and curses.has_colors():
                attr |= curses.A_REVERSE
            self._screen.addstr(0, col, label, attr)
        except curses.error:
            pass

    def refresh(self):
        self.check_deadline()

        old_y, old_x = self._screen.getyx()

        try:
            self._draw_header()
            self._draw_clock()
        finally:

            try:
                self._screen.move(old_y, old_x)
            except curses.error:
                pass

        return self._screen.refresh()

    def getstr(self, row, col, max_len=1023):
        """Read a line while continuously updating the deadline display.

        Unlike curses.getstr(), this cannot wait indefinitely for Enter.
        Input is ASCII/UTF-8-safe; length is limited in bytes, as with getstr.
        """
        self.check_deadline()
        height, width = self._screen.getmaxyx()
        if not (0 <= row < height and 0 <= col < width):
            raise curses.error('Input position outside terminal')
        buf = bytearray()

        curses.noecho()
        self._screen.timeout(self.POLL_MS)
        try:
            self._screen.move(row, col)
            while True:
                self.refresh()
                self.check_deadline()
                key = self._screen.getch()
                self.check_deadline()
                if key == -1 or key == curses.KEY_RESIZE:
                    continue
                if key in (10, 13, curses.KEY_ENTER):
                    return bytes(buf)
                if key in (curses.KEY_BACKSPACE, 127, 8):
                    if buf:
                        buf.pop()
                        self._screen.addstr(row, col, ' ' * min(max_len, width - col - 1))
                        self._screen.addstr(row, col, buf.decode('ascii', errors='ignore'))
                        self._screen.move(row, col + len(buf))
                    continue
                if 32 <= key <= 126 and len(buf) < max_len and col + len(buf) < width - 1:
                    buf.append(key)
                    self._screen.addch(row, col + len(buf) - 1, key)
        finally:
            self._screen.timeout(-1)

            curses.noecho()

    def get_wch(self):
        """Deadline-aware single-key input for any future puzzle prompts."""
        self._screen.timeout(self.POLL_MS)
        try:
            while True:
                self.refresh()
                self.check_deadline()
                try:
                    key = self._screen.get_wch()
                except curses.error:
                    continue
                self.check_deadline()
                return key
        finally:
            self._screen.timeout(-1)
