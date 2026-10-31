"""Title Screen Module for Titanic Escape.
Demonstrates:
- Spiky Iceberg with embedded menu on the left (Cols 0-27)
- Detailed Titanic with 4 funnels and portholes on the right (Cols 32-77)
- Bobbing ship animation (high/low tide)
- Moving ocean waves (Cols 28-79 on Row 11, full width Rows 12-23)
- Flying bird with flapping wings in the night sky
- Colour support with curses
- Strict 80x24 terminal constraint with auto-pause on resize
"""

try:
    import curses
except ImportError:
    curses = None

import os
import random
import sys
import time

WIDTH = 80
HEIGHT = 24

# Static Iceberg Art (Rows 0 to 11, Cols 0 to 27)
ICEBERG_LINES = [
    "    /\\",
    "   /  \\    /\\",
    "  /    \\  /  \\    /\\",
    " /      \\/    \\  /  \\",
    "/  TITANIC     \\/    \\",
    "|  ESCAPE      /      \\",
    "|             /        \\",
    "|  [C] Start   \\        \\",
    "|  [H] Help     \\        \\",
    "|  [Q] Quit      \\        \\",
    "|                 \\        \\",
    "\\__________________\\________\\",
]

# Detailed Titanic Silhouette (Cols 32 to 77)
# Note: Lower hull is at line 8, which gets submerged during low tide!
SHIP_LINES = [
    "                 |                     |",
    "               --+--                 --+--",
    "                 |  [##] [##] [##] [##]|",
    "                 |  |  | |  | |  | |  ||",
    "            __   |  |  | |  | |  | |  ||",
    "          _/__\\__|__|__|_|__|_|__|_|__||_",
    "        _/   o   o   o   o  o   o  o      \\",
    "  _____/___________________________________\\",
    " /   .   .   .   .   .   .   .   .   .   .  \\",
]

# Wave cycle pattern for ocean animation
WAVE_PATTERN = "~  ~  -  ^  ~  -  .  ~  "

# Base layout coordinates
BASE_ICEBERG_ROW = 6
BASE_SHIP_ROW = 9
SHIP_COL = 32
WATERLINE_ROW = 17

# Expanded background stars across the vast night sky
STARS = [
    (0, 5), (0, 18), (0, 35), (0, 62), (0, 74),
    (1, 12), (1, 28), (1, 40), (1, 68),
    (2, 8), (2, 22), (2, 33), (2, 60), (2, 72),
    (3, 4), (3, 16), (3, 30), (3, 65), (3, 76),
    (4, 10), (4, 25), (4, 38), (4, 70),
    (5, 6), (5, 20), (5, 44), (5, 75),
    (6, 35), (6, 52), (6, 68),
    (7, 40), (7, 60), (7, 74),
    (8, 33), (8, 77),
]


def setup_colours():
    """Initialise color pairs with black background fallback."""
    styles = {
        "ice": curses.A_BOLD,
        "text_title": curses.A_BOLD,
        "text_key": curses.A_BOLD,
        "text_normal": curses.A_NORMAL,
        "ship_mast": curses.A_NORMAL,
        "ship_funnel": curses.A_BOLD,
        "ship_porthole": curses.A_BOLD,
        "ship_hull": curses.A_NORMAL,
        "water": curses.A_NORMAL,
        "star": curses.A_DIM,
        "bird": curses.A_BOLD,
        "moon": curses.A_BOLD,
    }
    if not curses.has_colors():
        return styles

    try:
        curses.start_color()
        bg = curses.COLOR_BLACK
        try:
            curses.use_default_colors()
            bg = -1
        except curses.error:
            bg = curses.COLOR_BLACK

        # Pair 1: Cyan for Iceberg
        curses.init_pair(1, curses.COLOR_CYAN, bg)
        styles["ice"] = curses.color_pair(1) | curses.A_BOLD

        # Pair 2: Yellow for Key Prompts, Moon, and Portholes
        curses.init_pair(2, curses.COLOR_YELLOW, bg)
        styles["text_key"] = curses.color_pair(2) | curses.A_BOLD
        styles["ship_porthole"] = curses.color_pair(2) | curses.A_BOLD
        styles["moon"] = curses.color_pair(2) | curses.A_BOLD

        # Pair 3: Blue for Ocean Water
        curses.init_pair(3, curses.COLOR_BLUE, bg)
        styles["water"] = curses.color_pair(3)

        # Pair 4: Red for Ship Funnels
        curses.init_pair(4, curses.COLOR_RED, bg)
        styles["ship_funnel"] = curses.color_pair(4) | curses.A_BOLD

        # Pair 5: White for Crisp Text, Stars, Birds, Smoke, and Masts
        curses.init_pair(5, curses.COLOR_WHITE, bg)
        styles["text_title"] = curses.color_pair(5) | curses.A_BOLD
        styles["text_normal"] = curses.color_pair(5)
        styles["bird"] = curses.color_pair(5) | curses.A_BOLD
        styles["star"] = curses.color_pair(5) | curses.A_DIM
        styles["ship_mast"] = curses.color_pair(5)
        styles["ship_hull"] = curses.color_pair(5)
        styles["smoke_thick"] = curses.color_pair(5) | curses.A_BOLD
        styles["smoke_trail"] = curses.color_pair(5)

    except curses.error:
        pass

    return styles


def safe_addstr(screen, row, col, text, style=0):
    """Safely write a string without exceeding 80x24 bounds or wrapping."""
    if row < 0 or row >= HEIGHT or not text:
        return
    # Handle smooth clipping off the left edge of the screen
    if col < 0:
        if -col >= len(text):
            return
        text = text[-col:]
        col = 0
    if col >= WIDTH:
        return
    max_len = WIDTH - 1 - col
    if max_len <= 0:
        return
    clipped = text[:max_len]
    try:
        screen.addstr(row, col, clipped, style)
    except curses.error:
        pass


def draw_sky_and_stars(screen, styles):
    """Draw distant twinkling stars and crescent moon in the upper sky."""
    for row, col in STARS:
        safe_addstr(screen, row, col, ".", styles["star"])
    # Glowing crescent moon in the night sky
    safe_addstr(screen, 1, 50, "(", styles["moon"])


def draw_smoke(screen, ship_start_row, frame_count, styles):
    """Render billowing distinct smoke/steam plumes drifting from the four funnels."""
    # 3-frame churning animation cycle
    cycle = (frame_count // 2) % 3
    puff_r10 = ["( )", "() ", " ()"][cycle]
    puff_r9  = ["(~)", "(o)", "(~)"][cycle]
    puff_r8  = ["(@)", "(%)", "(@)"][cycle]
    wisp_r7  = ["~.~", ".-~", "~-."][cycle]

    # Funnels are located at cols 52, 57, 62, 67
    for fc in (52, 57, 62, 66):
        # Row 10 (directly above funnel): thick fresh steam
        safe_addstr(screen, ship_start_row + 1, fc, puff_r10, styles["smoke_thick"])
        # Row 9 (drifting +1 right): billow
        safe_addstr(screen, ship_start_row, fc + 1, puff_r9, styles["smoke_thick"])
        # Row 8 (drifting +2 right): expanding cloud
        safe_addstr(screen, ship_start_row - 1, fc + 2, puff_r8, styles["smoke_trail"])
        # Row 7 (drifting +4 right): trailing wisps
        safe_addstr(screen, ship_start_row - 2, fc + 4, wisp_r7, styles["smoke_trail"])


def draw_bird(screen, bird_state, frame_count, styles):
    """Render occasionally flying bird with flapping wings."""
    if not bird_state["active"]:
        return
    wings = "\\v/" if (frame_count // 2) % 2 == 0 else "^v^"
    safe_addstr(screen, bird_state["y"], bird_state["x"], wings, styles["bird"])


def draw_iceberg(screen, styles):
    """Draw the spiky iceberg with embedded title and menu."""
    for idx, line in enumerate(ICEBERG_LINES):
        safe_addstr(screen, BASE_ICEBERG_ROW + idx, 0, line, styles["ice"])

    # Overwrite embedded text labels with highlighted colours
    safe_addstr(screen, BASE_ICEBERG_ROW + 4, 3, "TITANIC", styles["text_title"])
    safe_addstr(screen, BASE_ICEBERG_ROW + 5, 3, "ESCAPE", styles["text_title"])

    # Menu items: [C] Start, [H] Help, [Q] Quit
    safe_addstr(screen, BASE_ICEBERG_ROW + 7, 3, "[C]", styles["text_key"])
    safe_addstr(screen, BASE_ICEBERG_ROW + 7, 7, "Start", styles["text_normal"])

    safe_addstr(screen, BASE_ICEBERG_ROW + 8, 3, "[H]", styles["text_key"])
    safe_addstr(screen, BASE_ICEBERG_ROW + 8, 7, "Help", styles["text_normal"])

    safe_addstr(screen, BASE_ICEBERG_ROW + 9, 3, "[Q]", styles["text_key"])
    safe_addstr(screen, BASE_ICEBERG_ROW + 9, 7, "Quit", styles["text_normal"])


def draw_ship(screen, ship_start_row, ship_start_col, styles):
    """Draw the Titanic with funnels, bridge, and portholes."""
    for idx, line in enumerate(SHIP_LINES):
        curr_row = ship_start_row + idx
        # Submerge any part of the ship that sinks into deep water (Row 18+)
        if curr_row > WATERLINE_ROW:
            continue

        if idx in (2, 3):  # Funnels
            safe_addstr(screen, curr_row, ship_start_col, line, styles["ship_funnel"])
        elif idx == 6:  # Portholes deck
            safe_addstr(screen, curr_row, ship_start_col, line, styles["ship_porthole"])
        else:
            safe_addstr(screen, curr_row, ship_start_col, line, styles["ship_hull"])


def draw_ocean(screen, frame_count, styles, bob_offset=0):
    """Draw ocean waves lapping against the waterline and deep ocean below."""
    # Row 17 (Waterline): Open water gap between Iceberg base (Col 28) and Ship bow (Col 32)
    offset_17 = frame_count % len(WAVE_PATTERN)
    wave_gap = (WAVE_PATTERN[offset_17:] + WAVE_PATTERN[:offset_17])[:4]
    safe_addstr(screen, WATERLINE_ROW, 28, wave_gap, styles["water"])
    # Open water behind the stern (Cols 77 to 79)
    safe_addstr(screen, WATERLINE_ROW, 77, wave_gap[:2], styles["water"])

    # Rows 18 to 23: Deep ocean waves (6 rows of water)
    for row in range(WATERLINE_ROW + 1, HEIGHT):
        offset = (frame_count * 2 + row * 3) % len(WAVE_PATTERN)
        wave_str = (WAVE_PATTERN[offset:] + WAVE_PATTERN[:offset]) * 6
        safe_addstr(screen, row, 0, wave_str[: WIDTH - 1], styles["water"])


def run_title_screen(screen):
    """Main loop for the animated title screen."""
    styles = setup_colours()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    screen.timeout(100)  # Polling interval: 100ms
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    frame_count = 0
    bird_state = {"active": False, "x": 75, "y": 2}

    while True:
        # Check terminal size
        actual_lines, actual_cols = screen.getmaxyx()
        if actual_lines < HEIGHT or actual_cols < WIDTH:
            screen.erase()
            safe_addstr(screen, 0, 0, "Window too small! Resize to at least 80 x 24.", styles["text_key"])
            safe_addstr(screen, 1, 0, f"Current size: {actual_cols} x {actual_lines}", styles["text_normal"])
            safe_addstr(screen, 2, 0, "Press [Q] to quit.", styles["text_normal"])
            screen.refresh()
            try:
                ch = screen.get_wch()
                if ch in ("q", "Q", "\x03"):
                    return "q"
            except curses.error:
                pass
            time.sleep(0.1)
            continue

        # Update bird state
        if not bird_state["active"]:
            if random.random() < 0.05:
                bird_state["active"] = True
                bird_state["x"] = 75
                bird_state["y"] = random.choice([2, 3, 4])
        else:
            bird_state["x"] -= 1
            if bird_state["x"] < -3:  # Only despawns when completely off the left edge!
                bird_state["active"] = False

        # Bobbing calculation: shifts by 1 row every ~0.6s
        bob_offset = 1 if (frame_count // 6) % 2 == 1 else 0
        current_ship_row = BASE_SHIP_ROW + bob_offset

        # Render frame
        screen.erase()
        draw_sky_and_stars(screen, styles)
        draw_smoke(screen, current_ship_row, frame_count, styles)
        draw_ship(screen, current_ship_row, SHIP_COL, styles)
        draw_iceberg(screen, styles)
        draw_bird(screen, bird_state, frame_count, styles)  # Drawn above iceberg so it never vanishes early!
        draw_ocean(screen, frame_count, styles, bob_offset)
        screen.refresh()

        frame_count += 1

        # Check user input (non-blocking)
        try:
            key = screen.get_wch()
        except curses.error:
            key = None

        if key is not None:
            if isinstance(key, str):
                key_lower = key.lower()
                if key_lower in ("c", "h", "q"):
                    return key_lower
            if key == curses.KEY_RESIZE:
                continue


def render_ansi_preview(frame_count=0, bob_offset=0, bird_x=60, bird_active=True):
    """Renders a single frame to a string using ANSI escape codes for testing outside curses."""
    grid = [[" "] * WIDTH for _ in range(HEIGHT)]
    color_grid = [[""] * WIDTH for _ in range(HEIGHT)]

    C_CYAN = "\033[96;1m"
    C_BLUE = "\033[94m"
    C_YELLOW = "\033[93;1m"
    C_RED = "\033[91;1m"
    C_WHITE = "\033[97;1m"
    C_DIM = "\033[90m"
    C_RESET = "\033[0m"

    # Stars
    for r, c in STARS:
        grid[r][c] = "."
        color_grid[r][c] = C_DIM

    # Moon
    grid[1][50] = "("
    color_grid[1][50] = C_YELLOW

    # Billowing distinct smoke/steam plumes above funnels
    ship_r = BASE_SHIP_ROW + bob_offset
    cycle = (frame_count // 2) % 3
    puff_r10 = ["( )", "() ", " ()"][cycle]
    puff_r9  = ["(~)", "(o)", "(~)"][cycle]
    puff_r8  = ["(@)", "(%)", "(@)"][cycle]
    wisp_r7  = ["~.~", ".-~", "~-."][cycle]

    for fc in (52, 57, 62, 66):
        for roff, text, col_style in (
            (1, puff_r10, C_WHITE),
            (0, puff_r9, C_WHITE),
            (-1, puff_r8, C_DIM),
            (-2, wisp_r7, C_DIM),
        ):
            sr = ship_r + roff
            sc = fc + (1 if roff == 0 else (2 if roff == -1 else (4 if roff == -2 else 0)))
            for i, ch in enumerate(text):
                c = sc + i
                if 0 <= sr < HEIGHT and 0 <= c < WIDTH and ch != " ":
                    grid[sr][c] = ch
                    color_grid[sr][c] = col_style

    # Waterline Row 17
    offset_17 = frame_count % len(WAVE_PATTERN)
    w_str_17 = (WAVE_PATTERN[offset_17:] + WAVE_PATTERN[:offset_17])
    for i in range(4):
        grid[WATERLINE_ROW][28 + i] = w_str_17[i]
        color_grid[WATERLINE_ROW][28 + i] = C_BLUE
    for i in range(2):
        grid[WATERLINE_ROW][77 + i] = w_str_17[i]
        color_grid[WATERLINE_ROW][77 + i] = C_BLUE

    # Waves rows 18-23
    for row in range(WATERLINE_ROW + 1, HEIGHT):
        offset = (frame_count * 2 + row * 3) % len(WAVE_PATTERN)
        w_str = (WAVE_PATTERN[offset:] + WAVE_PATTERN[:offset]) * 6
        for col in range(WIDTH - 1):
            grid[row][col] = w_str[col]
            color_grid[row][col] = C_BLUE

    # Ship
    ship_c = SHIP_COL
    for idx, line in enumerate(SHIP_LINES):
        curr_r = ship_r + idx
        if curr_r <= WATERLINE_ROW:
            col_style = C_WHITE
            if idx in (2, 3):
                col_style = C_RED
            elif idx == 6:
                col_style = C_YELLOW
            for i, ch in enumerate(line):
                c = ship_c + i
                if ch != " " and 0 <= c < WIDTH:
                    grid[curr_r][c] = ch
                    color_grid[curr_r][c] = col_style

    # Iceberg
    for r_idx, line in enumerate(ICEBERG_LINES):
        r = BASE_ICEBERG_ROW + r_idx
        for i, ch in enumerate(line):
            if 0 <= i < WIDTH:
                grid[r][i] = ch
                color_grid[r][i] = C_CYAN

    # Highlight Iceberg menu text
    def colorize_text(r, c, text, color):
        for i, ch in enumerate(text):
            if 0 <= c + i < WIDTH:
                grid[r][c + i] = ch
                color_grid[r][c + i] = color

    colorize_text(BASE_ICEBERG_ROW + 4, 3, "TITANIC", C_WHITE)
    colorize_text(BASE_ICEBERG_ROW + 5, 3, "ESCAPE", C_WHITE)
    colorize_text(BASE_ICEBERG_ROW + 7, 3, "[C]", C_YELLOW)
    colorize_text(BASE_ICEBERG_ROW + 7, 7, "Start", C_WHITE)
    colorize_text(BASE_ICEBERG_ROW + 8, 3, "[H]", C_YELLOW)
    colorize_text(BASE_ICEBERG_ROW + 8, 7, "Help", C_WHITE)
    colorize_text(BASE_ICEBERG_ROW + 9, 3, "[Q]", C_YELLOW)
    colorize_text(BASE_ICEBERG_ROW + 9, 7, "Quit", C_WHITE)

    # Bird (rendered on top so it never vanishes early)
    if bird_active:
        wings = "\\v/" if (frame_count // 2) % 2 == 0 else "^v^"
        for i, ch in enumerate(wings):
            c = bird_x + i
            if 0 <= c < WIDTH and 0 <= 2 < HEIGHT:
                grid[2][c] = ch
                color_grid[2][c] = C_WHITE

    # Build lines
    lines = []
    for r in range(HEIGHT):
        line_chars = []
        curr_color = ""
        for c in range(WIDTH):
            char_color = color_grid[r][c]
            if char_color != curr_color:
                line_chars.append(C_RESET if not char_color else char_color)
                curr_color = char_color
            line_chars.append(grid[r][c])
        if curr_color:
            line_chars.append(C_RESET)
        lines.append("".join(line_chars))

    return "\n".join(lines)


def main():
    if "--preview" in sys.argv or curses is None:
        print("=== TITANIC ESCAPE TITLE SCREEN (80x24 PREVIEW) ===")
        print(render_ansi_preview(frame_count=0, bob_offset=0, bird_x=60, bird_active=True))
        print("=" * 80)
        print("Note: To run the full interactive curses animation, execute inside Docker:")
        print("  docker compose run --rm game python title_screen.py")
        return

    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Run this in an interactive terminal (e.g. inside Docker).")
        return
    os.environ.pop("COLUMNS", None)
    os.environ.pop("LINES", None)
    curses.use_env(False)
    chosen = curses.wrapper(run_title_screen)
    print(f"\nYou selected: {chosen.upper()}")


if __name__ == "__main__":
    main()
