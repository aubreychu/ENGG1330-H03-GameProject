import curses
import random
import time

from title_screen import run_title_screen
from timed_screen import TimedScreen, RoomTimeExpired
from puzzles import (
    puzzle1, puzzle2, puzzle3, puzzle4, puzzle5,
    puzzle6, puzzle7, puzzle8, puzzle9, puzzle10,
    puzzle11, puzzle12, puzzle13, puzzle14, puzzle15,
)

BASE_ROOM_TIME = 60

CATALOG = [
    {"name": "Mines Board", "run": puzzle1.run_puzzle},
    {"name": "Stake Dice", "run": puzzle2.run_puzzle},
    {"name": "Treasure Chest", "run": puzzle3.run_puzzle},
    {"name": "Slot Machine", "run": puzzle4.run_puzzle},
    {"name": "Chill Session", "run": puzzle5.run_puzzle},
    {"name": "4-Digit Code", "run": puzzle6.run_puzzle},
    {"name": "Number Bomb", "run": puzzle7.run_puzzle},
    {"name": "Big or Small Dice", "run": puzzle8.run_puzzle},
    {"name": "Pattern Guess", "run": puzzle9.run_puzzle},
    {"name": "Nim (15 Sticks)", "run": puzzle10.run_puzzle},
    {"name": "Locked Door", "run": puzzle11.run_puzzle},
    {"name": "Leaking Pipe", "run": puzzle12.run_puzzle},
    {"name": "Dark Storage Room", "run": puzzle13.run_puzzle},
    {"name": "Five Identical Doors", "run": puzzle14.run_puzzle},
    {"name": "Life Jacket Locker", "run": puzzle15.run_puzzle},
]


def show_help_screen(scr):
    # TODO: make this look less ugly later if time permits
    scr.timeout(-1)
    scr.erase()
    scr.addstr(2, 2, "=== TITANIC ESCAPE | HOW TO PLAY ===")
    scr.addstr(3, 2, "-" * 70)
    scr.addstr(5, 2, "The RMS Titanic has struck an iceberg and is rapidly taking on water!")
    scr.addstr(7, 2, "OBJECTIVE:")
    scr.addstr(8, 4, "- Ascend through 6 randomized compartments to reach the Boat Deck.")
    scr.addstr(9, 4, "- Solve the puzzle in each room to unlock the way forward.")
    scr.addstr(11, 2, "CONTROLS:")
    scr.addstr(12, 4, "- Follow the on-screen prompts in each room.")
    scr.addstr(13, 4, "- Type your answer and press [ENTER] to submit.")
    scr.addstr(15, 2, "WIN / LOSS:")
    scr.addstr(16, 4, "- Clear all 6 rooms to board a lifeboat and survive!")
    scr.addstr(17, 4, "- Failing a room or running out of time ends the game.")
    scr.addstr(19, 2, "- Remaining time is carried over to the next room.")
    scr.addstr(21, 2, "Press any key to return to the Title Screen...")
    scr.refresh()
    scr.get_wch()


def show_scene(screen, title, message, cleared, total=6, stats=None):
    screen.timeout(-1)
    screen.erase()

    h, w = screen.getmaxyx()

    def draw(row, text, style=0):
        if row >= h or row < 0:
            return
        text = str(text)[:max(0, w - 2)]
        col = max(0, (w - len(text)) // 2)
        try:
            screen.addstr(row, col, text, style)
        except curses.error:
            pass

    draw(3, "=" * 54)
    draw(5, "T I T A N I C   E S C A P E", curses.A_BOLD)
    draw(7, title, curses.A_BOLD)
    draw(9, message)

    draw(12, "ESCAPE PROGRESS")
    progress = " ".join(
        "[#]" if i < cleared else "[ ]"
        for i in range(total)
    )
    draw(14, progress, curses.A_BOLD)
    draw(15, f"{cleared} / {total} COMPARTMENTS CLEARED")

    if stats:
        draw(18, stats)

    draw(20, "=" * 54)
    draw(22, "Press any key to continue...")

    curses.noecho()
    screen.timeout(-1)
    screen.refresh()

    curses.flushinp()
    screen.getch()


def generate_rooms(catalog, num_rooms=6):
    chill = next((r for r in catalog if r["name"] == "Chill Session"), None)
    if chill is None or num_rooms <= 3:
        pool = [r for r in catalog if r is not chill]
        return random.sample(pool, k=num_rooms)
    chosen = random.sample(catalog, k=num_rooms)
    if chill in chosen:
        chosen.remove(chill)
        chosen.insert(random.randrange(3, num_rooms), chill)
    return chosen


def show_game_over(screen, timed_out, allowedTime=0, elapsed=0,
                   cleared=0, total=6):
    if timed_out:
        show_scene(
            screen,
            title="TIME EXPIRED!",
            message="The compartment flooded. The Titanic sinks...",
            cleared=cleared,
            total=total,
            stats=f"Time limit: {int(allowedTime)}s"
        )
    else:
        show_scene(
            screen,
            title="GAME OVER!",
            message="You failed the puzzle. The ship is sinking!",
            cleared=cleared,
            total=total,
            stats=f"{cleared} compartments cleared."
        )


def play_game(screen):
    curses.curs_set(0)
    while True:
        choice = run_title_screen(screen)
        screen.timeout(-1)
        if choice == "q":
            return False
        if choice == "h":
            show_help_screen(screen)
        elif choice == "c":
            break

    run = generate_rooms(CATALOG, num_rooms=6)
    extraTime = 0.0

    for idx, room in enumerate(run, start=1):
        screen.erase()
        allowedTime = BASE_ROOM_TIME + extraTime
        screen.addstr(0, 2, f"=== TITANIC ESCAPE | Room {idx} of {len(run)} ===")
        screen.addstr(1, 2, f"Location: {room['name']}")
        screen.addstr(2, 2, "-" * 70)
        screen.refresh()

        if room["name"] == "Chill Session":
            try:
                passed = room["run"](screen)
            finally:
                screen.timeout(-1)
                curses.noecho()

            elapsed = 0.0

        else:
            timed_screen = TimedScreen(
                screen,
                allowedTime,
                room_name=room["name"],
                room_number=idx,
                total_rooms=len(run)
            )

            started = time.monotonic()

            try:
                passed = room["run"](timed_screen)
                timed_screen.check_deadline()

            except RoomTimeExpired:
                elapsed = time.monotonic() - started

                show_game_over(
                    screen,
                    timed_out=True,
                    allowedTime=allowedTime,
                    elapsed=elapsed,
                    cleared=idx - 1,
                    total=len(run)
                )
                return False

            finally:
                screen.timeout(-1)
                curses.noecho()

            elapsed = time.monotonic() - started
        
        if not passed:
            show_game_over(
                screen,
                timed_out=False,
                cleared=idx - 1,
                total=len(run)
            )
            return False
            
        surplus = max(0.0, allowedTime - elapsed)
        extraTime = surplus

        if idx < len(run):
            if idx < len(run):
                show_scene(
                    screen,
                    title=f"COMPARTMENT {idx} CLEARED!",
                    message="You are one step closer to the Boat Deck!",
                    cleared=idx,
                    total=len(run),
                    stats=(
                        f"Time spent: {int(elapsed)}s | "
                        f"BONUS TIME EARNED: +{int(surplus)}s | "
                        f"Next room: {int(BASE_ROOM_TIME + extraTime)}s"
        )
    )

    show_scene(
        screen,
        title="YOU SURVIVED!",
        message="You reached the Boat Deck and escaped on a lifeboat!",
        cleared=len(run),
        total=len(run),
        stats=f"Remaining time: {int(extraTime)}s"
    )

    return True


if __name__ == "__main__":
    curses.wrapper(play_game)