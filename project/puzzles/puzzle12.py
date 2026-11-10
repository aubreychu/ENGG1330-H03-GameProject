# Puzzle will involve finding a leaking pipe and performing a pattern of turns to stop the leak
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
    screen.move(row, 0)
    screen.clrtoeol()

    screen.addstr(row, col, prompt)
    screen.refresh()
    curses.echo()
    curses.curs_set(1)
    raw = screen.getstr(row, col + len(prompt), 25)
    curses.noecho()
    curses.curs_set(0)
    return raw.decode("utf-8", errors="ignore").strip()


def run_puzzle(screen):
    message = (
        "You stumble across a leaking pipe!\n"
        "Stop the leaking before the entire room floods, and continue your escape!\n"
        "A series of numbers will briefly display, showing how to turn the valve.\n"
        "Once prompted, enter this series to show you know how to fix the leak!"
    )
    type_text(screen, 4, 2, message, delay=0.01)

    result = False
    while result == False:
        # Clear interaction area (Rows 9 to 16)
        for r in range(9, 17):
            screen.move(r, 0)
            screen.clrtoeol()

        nums = random.choices(range(10), k=8)
        code = "".join(str(num) for num in nums)

        screen.addstr(9, 2, "The code is: " + str(code))
        screen.refresh()
        time.sleep(2.5)

        # Clear the code from screen
        screen.move(9, 0)
        screen.clrtoeol()
        screen.refresh()
        flag = False
        #Input/Input validation
        while flag == False:
            guess = get_input(screen, 11, 2, "Enter the sequence: ")
            flag = True
            if len(guess) == 8 and guess.isdigit():
                break

            msg = "Please enter exactly 8 digits (0-9)!"
            type_text(screen, 13, 2, msg, delay=0.01)
            time.sleep(1.5)

            screen.move(13, 0)
            screen.clrtoeol()
        if guess == str(code):
            result = True
            msg = (
                "The valve makes a sudden shutting sound and the leak ends!\n"
                "You may now continue your escape!"
            )
            type_text(screen, 13, 2, msg, delay=0.01)
            time.sleep(1.5)
        else:
            msg = (
                "Nothing changes, the water is still gushing out!\n"
                "Try again."
            )
            type_text(screen, 13, 2, msg, delay=0.01)
            time.sleep(1.5)

    return result

if __name__ == "__main__":
    curses.wrapper(run_puzzle)