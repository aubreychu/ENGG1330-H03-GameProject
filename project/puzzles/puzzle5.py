import curses
import time


def type_text(screen, row, col, text, delay=0.02):
    """Draws text with a typewriter effect within 80x24 bounds."""
    r = row
    screen.move(r, col)
    for char in text:
        if char == "\n":
            r += 1
            if r < 23:
                screen.move(r, col)
        else:
            if r < 23:
                screen.addstr(char)
                screen.refresh()
                time.sleep(delay)


def get_input(screen, row, col, prompt, max_len=5):
    """Prompts the user inside curses."""
    screen.move(row, 0)
    screen.clrtoeol()
    screen.addstr(row, col, prompt)
    screen.refresh()
    curses.echo()
    curses.curs_set(1)
    raw = screen.getstr(row, col + len(prompt), max_len)
    curses.noecho()
    curses.curs_set(0)
    return raw.decode("utf-8", errors="ignore").strip()


def run_puzzle(screen):
    curses.curs_set(0)
    screen.addstr(4, 2, "=== CHILL SESSION (｡･ω･｡) ===")
    get_input(screen, 5, 2, "Press ENTER to take a little break...", max_len=1)

    screen.move(5, 0)
    screen.clrtoeol()

    # Compacted to 15 lines (Rows 5 to 19) so the entire message fits 80x24
    message = (
        "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧\n"
        "Heyyy! You've been doing pretty well so far!\n"
        "After all those games, you deserve a little break. (´｡• ᵕ •｡`) ♡\n"
        "Imagine yourself sitting in a cozy cafe.\n"
        "It's raining softly outside. ☂\n"
        "A warm cup of hot chocolate sits beside you. (っ˘ڡ˘ς) ☕\n"
        "There's no timer. No money to lose. No decisions to make.\n"
        "Just the gentle sound of rain, and a moment to yourself. ( ˘ω˘ )\n"
        "...\n"
        "You take another sip of your drink. The rain begins to slow down.\n"
        "A little sunlight peeks through the clouds. ☀\n"
        "Sometimes, it's nice to do absolutely nothing. (｡•̀ᴗ-)✧\n"
        "Anyway, your break is almost over.\n"
        "There are still more adventures waiting for you!\n"
        "Take your time. No rush. ♡  ヾ(＾▽＾)ﾉ"
    )

    type_text(screen, 5, 2, message, delay=0.02)

    get_input(
        screen, 21, 2,
        "Press ENTER whenever you're ready to continue... ",
        max_len=1
    )
    return True


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
