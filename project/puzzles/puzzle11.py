
import curses
import random
import time


def type_text(screen, row, col, text, delay=0.01):
    """Draw text with a typewriter effect."""
    r, c = row, col

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
    """Get user input and clear the input line."""
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
    curses.curs_set(0)

    message = (
        "You've arrived at a dead end! The only way out is the locked door.\n"
        "The keypad has numbers 0 to 9. Use hints to open it and escape!\n"
        "Beware: each failed attempt resets the password.\n"
        "*Some hints refer to length and content, others do not."
    )

    type_text(screen, 4, 2, message)

    # Password and hint pairs
    passwords = [
        ("011235", "The past dictates the future. Who's scared of 7?"),
        ("321", "Go!"),
        ("1000", "8 in binary"),
        ("123456", "As simple as it gets. And as deep as you go when it ends"),
        ("00000", "No magnitude, but the length of 'hello'.")
        ("777", "The number of luck, and you'll need it to win lot!"),
    ]

    while True:
        # Clear interaction area
        for r in range(9, 16):
            screen.move(r, 0)
            screen.clrtoeol()

        # Generate a password for this round
        key = random.randint(0, 4)
        password, hint = passwords[key]

        # Display hint BEFORE guessing
        screen.addstr(9, 2, "Hint: " + hint)
        screen.refresh()

        # Input validation
        while True:
            guess = get_input(screen, 11, 2, "Enter your guess: ")

            # Clear previous error message
            screen.move(13, 0)
            screen.clrtoeol()

            if guess.isdigit():
                break

            type_text(
                screen, 13, 2,
                "Please enter valid numeric input!"
            )
            time.sleep(1.5)

        # Check password
        if guess == password:
            type_text(
                screen, 13, 2,
                "Correct! The door opens! Good luck on the rest of your escape!"
            )
            time.sleep(1.5)
            return True

        else:
            type_text(
                screen, 13, 2,
                "Wrong password! The password is resetting..."
            )
            time.sleep(2)


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
