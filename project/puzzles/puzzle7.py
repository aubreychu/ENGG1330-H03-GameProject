import curses
import random
import time


def get_input(screen, row, col, prompt, max_len=15):
    """Prompts the user for a text string inside curses."""
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

    # Game rules (Rows 4 to 11, all under 75 columns)
    screen.addstr(4, 2, "Welcome to NUMBER BOMB!")
    screen.addstr(5, 2, "A secret bomb number is hidden in a range (0-100).")
    screen.addstr(6, 2, "Players take turns guessing a number. After each guess:")
    screen.addstr(7, 4, "- Too low  -> everything up to your guess is eliminated")
    screen.addstr(8, 4, "- Too high -> everything from your guess upward is eliminated")
    screen.addstr(9, 2, "Guess the hidden number within 10 tries to win. Good luck!")
    screen.refresh()

    x = random.randint(0, 100)
    times = 10

    while times > 0:
        for r in range(12, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        screen.addstr(12, 2, f"Attempts remaining: {times}")
        raw = get_input(screen, 14, 2, "Enter your guess (0-100): ")

        if not raw.isdigit():
            screen.addstr(16, 2, "Please enter a valid number!")
            screen.refresh()
            time.sleep(1.0)
            continue

        y = int(raw)
        if y > x:
            screen.addstr(16, 2, "Guess it smaller")
            screen.refresh()
            times -= 1
            time.sleep(1.0)
        elif y < x:
            screen.addstr(16, 2, "Guess it higher")
            screen.refresh()
            times -= 1
            time.sleep(1.0)
        else:
            screen.addstr(16, 2, "Congradulation! You get it right")
            screen.refresh()
            time.sleep(1.5)
            return True

    screen.addstr(18, 2, f"Out of attempts! The secret number was {x}.")
    screen.refresh()
    time.sleep(1.5)
    return False


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
