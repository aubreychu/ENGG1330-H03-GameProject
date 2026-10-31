# This puzzle will involve the user opening the correct door in order to progress along the game
import curses
import random
import time


def type_text(screen, row, col, text, delay=0.01):
    """Draws text with a fast typewriter effect at a given coordinate."""
    r = row
    c = col
    for char in text:
        if char == "\n":
            r += 1
            c = col
        else:
            if c >= 78:
                r += 1
                c = col
            if r < 23:
                screen.addch(r, c, char)
                screen.refresh()
                time.sleep(delay)
            c += 1


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
    message = (
        "You arrive upon 5 identical doors!\n"
        "Open the right door to continue your escape!\n"
        "Beware, every failed attempt causes the correct door to change location."
    )
    type_text(screen, 4, 2, message, delay=0.01)

    result = False
    while result == False:
        # Clear interaction area (Rows 8 to 22)
        for r in range(8, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        current = random.randint(1, 5)

        # Draw 5 doors on Rows 8 to 12
        screen.addstr(8, 2, " ___   ___   ___   ___   ___")
        screen.addstr(9, 2, "|   | |   | |   | |   | |   |")
        screen.addstr(10, 2, "| 1 | | 2 | | 3 | | 4 | | 5 |")
        screen.addstr(11, 2, "|   | |   | |   | |   | |   |")
        screen.addstr(12, 2, "|___| |___| |___| |___| |___|")
        screen.refresh()

        raw_guess = get_input(screen, 14, 2, "Which door leads to your escape: ")
        if not raw_guess.isdigit():
            type_text(screen, 16, 2, "Please enter a door number (1-5)!", delay=0.01)
            time.sleep(1.0)
            continue

        guess = int(raw_guess)

        if guess == current:
            msg = "Hurray the door leads to a corridor, the key to your escape!"
            type_text(screen, 16, 2, msg, delay=0.01)
            time.sleep(1.5)
            result = True
        else:
            msg = "Oh no, the door leads to a dead end, try again!"
            type_text(screen, 16, 2, msg, delay=0.01)
            time.sleep(1.2)

    return result


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
