# Puzzle will involve trying to open a locked door where the password changes
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
    raw = screen.getstr(row, col + len(prompt), 25)
    curses.noecho()
    curses.curs_set(0)
    return raw.decode("utf-8", errors="ignore").strip()


def run_puzzle(screen):
    key = random.randint(1, 5)
    result = False

    message = (
        "You've arrived at a dead end! The only way out is the locked door.\n"
        "The keypad has numbers 0 to 9. Use hints to open it and escape!\n"
        "Beware: each failed attempt resets the password.\n"
        "*Some hints refer to length and content, others do not."
    )

    # Type out intro story within Rows 4 to 7
    type_text(screen, 4, 2, message, delay=0.01)

    # A series of passwords with corresponding hints
    pas1 = "011235"
    hint1 = "The past dictates the future. Who's scared of 7?"
    pas2 = "321"
    hint2 = "Go!"
    pas3 = "1000"
    hint3 = "8 in binary"
    pas4 = "123456"
    hint4 = "As simple as it gets. And as deep as you go when it ends"
    pas5 = "00000"
    hint5 = "This number has no magnuitude, yet it take up just as much space as the word 'hello'"

    # Loop that runs until the user has correctly guessed the password
    while result == False:
        # Clear interaction area (Rows 9 to 15) for the new attempt
        for r in range(9, 16):
            screen.move(r, 0)
            screen.clrtoeol()

        key = random.randint(1, 5)
        if key == 1:
            screen.addstr(9, 2, "Hint: " + hint1)
            guess = get_input(screen, 11, 2, "Enter your guess: ")
            if guess == pas1:
                result = True
                msg = "Correct! The door opens! Good luck on the rest of your escape!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.5)
            else:
                msg = "The door still doesn't budge! Try again!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.2)
        elif key == 2:
            screen.addstr(9, 2, "Hint: " + hint2)
            guess = get_input(screen, 11, 2, "Enter your guess: ")
            if guess == pas2:
                result = True
                msg = "Correct! The door opens! Good luck on the rest of your escape!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.5)
            else:
                msg = "The door still doesn't budge! Try again!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.2)
        elif key == 3:
            screen.addstr(9, 2, "Hint: " + hint3)
            guess = get_input(screen, 11, 2, "Enter your guess: ")
            if guess == pas3:
                result = True
                msg = "Correct! The door opens! Good luck on the rest of your escape!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.5)
            else:
                msg = "The door still doesn't budge! Try again!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.2)
        elif key == 4:
            screen.addstr(9, 2, "Hint: " + hint4)
            guess = get_input(screen, 11, 2, "Enter your guess: ")
            if guess == pas4:
                result = True
                msg = "Correct! The door opens! Good luck on the rest of your escape!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.5)
            else:
                msg = "The door still doesn't budge! Try again!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.2)
        elif key == 5:
            screen.addstr(9, 2, "Hint: This number has no magnuitude, yet it take up")
            screen.addstr(10, 8, "just as much space as the word 'hello'")
            guess = get_input(screen, 11, 2, "Enter your guess: ")
            if guess == pas5:
                result = True
                msg = "Correct! The door opens! Good luck on the rest of your escape!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.5)
            else:
                msg = "The door still doesn't budge! Try again!"
                type_text(screen, 13, 2, msg, delay=0.01)
                time.sleep(1.2)

    return result
