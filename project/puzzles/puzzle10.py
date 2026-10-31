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

    screen.addstr(4, 2, "Nim")
    screen.addstr(5, 2, "There are 15 sticks.")
    screen.addstr(6, 2, "Take turns removing 1, 2, or 3 sticks.")
    screen.addstr(7, 2, "Whoever takes the LAST stick LOSES. You go first.")
    screen.refresh()

    sticks = 15

    while sticks > 0:
        for r in range(9, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        screen.addstr(9, 2, f"Sticks left: {sticks}   ({'| ' * sticks})")
        screen.refresh()

        # Player turn
        while True:
            take = get_input(screen, 11, 2, "How many do you take? (1-3): ")
            if take in ("1", "2", "3"):
                take = int(take)
                if take <= sticks:
                    screen.move(12, 0)
                    screen.clrtoeol()
                    break
            screen.addstr(12, 2, "Take 1, 2, or 3 (and not more than remain)")
            screen.refresh()

        sticks -= take
        screen.addstr(14, 2, f"You take {take}. Sticks left: {sticks}")
        screen.refresh()

        if sticks == 0:
            screen.addstr(16, 2, "You took the last stick. Computer wins!")
            screen.refresh()
            time.sleep(1.5)
            return False

        time.sleep(0.8)

        # Computer turn - smart play
        if sticks % 4 == 0:
            comp_take = random.randint(1, 3)
        else:
            comp_take = sticks % 4
        if comp_take > sticks:
            comp_take = sticks

        sticks -= comp_take
        screen.addstr(16, 2, f"Computer takes {comp_take}. Sticks left: {sticks}")
        screen.refresh()

        if sticks == 0:
            screen.addstr(18, 2, "Computer took the last stick. You win!")
            screen.refresh()
            time.sleep(1.5)
            return True

        time.sleep(1.2)

    return False


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
