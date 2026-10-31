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

    screen.addstr(4, 2, "Pattern Guess")
    screen.addstr(5, 2, "I'll show you a sequence. Guess the next number!")
    screen.addstr(6, 2, "First to get 7 correct wins")
    screen.refresh()

    rules = [
        ("+2",  lambda x: x + 2),
        ("+3",  lambda x: x + 3),
        ("+5",  lambda x: x + 5),
        ("×2",  lambda x: x * 2),
        ("×3",  lambda x: x * 3),
        ("-1",  lambda x: x - 1),
        ("+10", lambda x: x + 10),
        ("×2+1", lambda x: x * 2 + 1),
    ]

    correct = 0

    while correct < 7:
        for r in range(8, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        name, rule = random.choice(rules)
        start = random.randint(1, 10)

        seq = [start]
        for i in range(3):
            seq.append(rule(seq[-1]))

        screen.addstr(8, 2, f"Progress: {correct}/7 correct")
        screen.addstr(10, 2, f"Sequence: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ?")
        answer = get_input(screen, 12, 2, "Next number: ")

        if not answer.lstrip("-").isdigit() or answer in ("", "-"):
            screen.addstr(14, 2, "Please type a number")
            screen.refresh()
            time.sleep(1.0)
            continue

        expected = rule(seq[-1])
        if int(answer) == expected:
            correct += 1
            screen.addstr(14, 2, f"Correct! ({correct}/7)")
        else:
            screen.addstr(14, 2, f"Wrong! The answer was {expected}  ({correct}/7)")

        screen.refresh()
        time.sleep(1.1)

    screen.addstr(17, 2, "You got 7 correct! You win!")
    screen.refresh()
    time.sleep(1.5)
    return True


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
