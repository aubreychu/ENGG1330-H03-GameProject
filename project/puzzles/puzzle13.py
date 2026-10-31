# Puzzle will involve the user finding a key in a dark room
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
            screen.addch(r, c, char)
            screen.refresh()
            time.sleep(delay)
            c += 1


def get_input(screen, row, col, prompt):
    """Prompts the user for a text string inside curses."""
    screen.addstr(row, col, prompt)
    screen.refresh()
    curses.echo()
    curses.curs_set(1)
    raw = screen.getstr(row, col + len(prompt), 15)
    curses.noecho()
    curses.curs_set(0)
    return raw.decode("utf-8", errors="ignore").strip()


def run_puzzle(screen):
    message = (
        "You open a door and enter a dark room.\n"
        "Find the key to open the door and continue your escape!\n"
        "A matrix will be displayed with 0s and a single 'o' (the key).\n"
        "Locate the key and enter its row and column (1-10)."
    )
    type_text(screen, 4, 2, message, delay=0.01)

    result = False
    while result == False:
        # Clear interaction and matrix area (Rows 8 to 23)
        for r in range(8, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        row = random.randint(0, 9)
        col = random.randint(0, 9)

        # Draw the 10x10 matrix (Rows 8 to 17, centered at Column 25)
        for i in range(10):
            line = ""
            for j in range(10):
                if i == row and j == col:
                    line += "o "
                else:
                    line += "0 "
            screen.addstr(8 + i, 25, line)

        screen.refresh()

        gRow = get_input(screen, 18, 2, "Enter the row: ")
        gCol = get_input(screen, 19, 2, "Enter the column: ")

        if gRow == str(row + 1) and gCol == str(col + 1):
            result = True
            msg = (
                "The key was found!\n"
                "The door opens and you continue on your epic escape!"
            )
            type_text(screen, 21, 2, msg, delay=0.01)
            time.sleep(1.5)
        else:
            msg = "Unlucky, the key wasn't there!\nTry again."
            type_text(screen, 21, 2, msg, delay=0.01)
            time.sleep(1.5)

    return result
