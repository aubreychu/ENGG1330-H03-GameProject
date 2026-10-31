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

    # Game rules formatted strictly within 75 columns (Rows 4 to 8)
    screen.addstr(4, 2, "1. The computer generates a 4-digit number (with repeated digits).")
    screen.addstr(5, 2, "2. The player has 10 attempts to guess the number.")
    screen.addstr(6, 2, "3. A = right digit & position; B = right digit, wrong position.")
    screen.addstr(7, 2, "4. Win by guessing all four digits correctly (4A0B).")
    screen.addstr(8, 2, "5. If all attempts are used, the game ends and the answer is shown.")
    screen.refresh()

    answer = "".join(random.choices("0123456789", k=4))
    attempts_left = 10
    attempt_num = 0

    while attempts_left > 0:
        for r in range(16, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        tryy = get_input(
            screen, 16, 2,
            f"Last {attempts_left} times, please input a 4-digit number: "
        )

        if len(tryy) != 4 or not tryy.isdigit():
            screen.addstr(18, 2, "Please input a 4-digit number!")
            screen.refresh()
            time.sleep(1.0)
            continue

        A = 0
        B = 0
        answer_list = list(answer)
        guess_list = list(tryy)

        for i in range(4):
            if guess_list[i] == answer_list[i]:
                A += 1
                answer_list[i] = None
                guess_list[i] = None

        for i in range(4):
            if guess_list[i] is not None and guess_list[i] in answer_list:
                B += 1
                answer_list[answer_list.index(guess_list[i])] = None

        # Record guess history in two compact columns on Rows 10 to 14
        hist_row = 10 + (attempt_num % 5)
        hist_col = 2 if attempt_num < 5 else 38
        screen.addstr(hist_row, hist_col, f"#{attempt_num + 1:2d}: {tryy} -> {A}A{B}B")
        attempt_num += 1

        screen.addstr(18, 2, f"Result: {A}A{B}B")
        screen.refresh()

        if A == 4:
            screen.addstr(20, 2, f"Congratulation, you get it right, the answer is {answer}")
            screen.refresh()
            time.sleep(1.5)
            return True

        attempts_left -= 1
        time.sleep(0.6)

    screen.addstr(20, 2, f"Game over, the answer is {answer}")
    screen.refresh()
    time.sleep(1.5)
    return False


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
