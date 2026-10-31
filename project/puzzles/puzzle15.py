# This puzzle will involve the user opening the life jacket locker
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
    # Formatted across Rows 4 to 10 so every line stays strictly under 75 columns
    message = (
        "You find yourself in front of a mysterious locker.\n"
        "When you approach it you realize it contains life jackets!\n"
        "Excited by your discovery you try opening it, but it remains locked!\n"
        "Complete the sequence of turns on the dial to access the safety vest.\n"
        "Perform the calculations displayed: if the result is odd turn right,\n"
        "otherwise turn it left.\n"
        "Careful: wrong entries cause the sequence to fail at the end!"
    )
    type_text(screen, 4, 2, message, delay=0.01)

    result = False
    while result == False:
        for r in range(12, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        result = True
        for step in range(5):
            for r in range(12, 18):
                screen.move(r, 0)
                screen.clrtoeol()

            sequence = [random.randint(1, 10) for _ in range(5)]
            output = ""
            for num in sequence:
                output = output + str(num) + " + "

            total_sum = 0
            for j in range(len(sequence)):
                total_sum += sequence[j]

            screen.addstr(12, 2, f"Turn {step + 1} of 5:")
            screen.addstr(13, 2, output[:-2])
            screen.refresh()

            answer = get_input(
                screen, 15, 2,
                "Enter 'r' for right and 'l' for left: "
            ).lower()

            if total_sum % 2 == 1:
                if answer != "r":
                    result = False
            else:
                if answer != "l":
                    result = False

        if result == False:
            msg = "The sequence wasn't correct!\nTry again!"
            type_text(screen, 18, 2, msg, delay=0.01)
            time.sleep(1.2)

    msg = "Hurray!!!\nThe locker opens, grab a vest and continue with your escape!"
    type_text(screen, 18, 2, msg, delay=0.01)
    time.sleep(1.5)
    return True


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
