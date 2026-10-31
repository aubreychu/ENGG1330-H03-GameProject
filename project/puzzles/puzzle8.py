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

    screen.addstr(4, 2, "Guess Big or Small")
    screen.addstr(5, 2, "Roll two dice, sum of pips:")
    screen.addstr(6, 2, "  Small=2~6   Big=8~12   7=no points")
    screen.addstr(7, 2, "First to win 5 rounds wins the match")
    screen.refresh()

    player = 0
    computer = 0

    while player < 5 and computer < 5:
        for r in range(9, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        screen.addstr(9, 2, f"Current Score -> You {player} : {computer} Computer")
        player_input = get_input(screen, 11, 2, "big or small: ").lower()

        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        total = d1 + d2
        screen.addstr(13, 2, f"Dice roll: {d1} + {d2} = {total}")

        if total == 7:
            screen.addstr(15, 2, "7 - no points")
        elif (total > 7 and player_input == "big") or (total < 7 and player_input == "small"):
            player += 1
            screen.addstr(15, 2, f"You win the round!  You {player} : {computer} Computer")
        else:
            computer += 1
            screen.addstr(15, 2, f"Computer wins the round!  You {player} : {computer} Computer")

        screen.refresh()
        time.sleep(1.2)

    if player == 5:
        screen.addstr(18, 2, "Congratulations! You win the match!")
        screen.refresh()
        time.sleep(1.5)
        return True
    else:
        screen.addstr(18, 2, "Computer wins the match. Better luck next time!")
        screen.refresh()
        time.sleep(1.5)
        return False


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
