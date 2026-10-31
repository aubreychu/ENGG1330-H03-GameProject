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
    money = 100.0
    target = random.randint(300, 600)

    screen.addstr(4, 2, "=== STAKE DICE PUZZLE ===")
    screen.addstr(5, 2, "Reach the target without going bankrupt! Dice: 0.00-99.99 (Edge: 1%)")
    screen.refresh()

    round_number = 0

    while money > 0 and money < target:
        round_number += 1

        # Clear round workspace (Rows 7 to 22)
        for r in range(7, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        screen.addstr(7, 2, f"=== ROUND {round_number} | Balance: ${money:.2f} | Target: ${target} ===")
        screen.refresh()

        # Choose bet amount
        while True:
            raw_bet = get_input(screen, 9, 2, "Enter bet amount: $")
            try:
                bet = float(raw_bet)
                if 0 < bet <= money:
                    screen.move(10, 0)
                    screen.clrtoeol()
                    break
                screen.addstr(10, 2, "Invalid bet amount!")
                screen.refresh()
            except ValueError:
                screen.addstr(10, 2, "Please enter a valid number.")
                screen.refresh()

        # Choose dice threshold
        while True:
            raw_thresh = get_input(screen, 10, 2, "Enter dice threshold (2-98): ")
            try:
                threshold = float(raw_thresh)
                if 2 <= threshold <= 98:
                    screen.move(11, 0)
                    screen.clrtoeol()
                    break
                screen.addstr(11, 2, "Threshold must be between 2 and 98!")
                screen.refresh()
            except ValueError:
                screen.addstr(11, 2, "Please enter a valid number.")
                screen.refresh()

        threshold = round(threshold, 2)
        under_chance = threshold
        over_chance = 100 - threshold

        under_multiplier = 99 / under_chance
        over_multiplier = 99 / over_chance

        under_profit = bet * (under_multiplier - 1)
        over_profit = bet * (over_multiplier - 1)

        screen.addstr(12, 2, "AVAILABLE BETS:")
        screen.addstr(
            13, 2,
            f"[U] UNDER {threshold:.2f} | Win: {under_chance:.2f}% | "
            f"Mult: {under_multiplier:.4f}x | Profit: +${under_profit:.2f}"
        )
        screen.addstr(
            14, 2,
            f"[O] OVER  {threshold:.2f} | Win: {over_chance:.2f}% | "
            f"Mult: {over_multiplier:.4f}x | Profit: +${over_profit:.2f}"
        )
        screen.refresh()

        # Choose roll direction
        while True:
            direction = get_input(screen, 16, 2, "Roll [O]ver or [U]nder? ").lower()
            if direction in ["o", "u"]:
                break
            screen.addstr(17, 2, "Invalid choice! Enter O or U.")
            screen.refresh()

        screen.move(17, 0)
        screen.clrtoeol()
        if direction == "u":
            profit = under_profit
            choice_str = f"UNDER {threshold:.2f}"
        else:
            profit = over_profit
            choice_str = f"OVER {threshold:.2f}"

        screen.addstr(17, 2, f"Chose {choice_str} | Bet: ${bet:.2f} | Potential profit: +${profit:.2f}")
        get_input(screen, 18, 2, "Press ENTER to roll...", max_len=1)

        screen.move(18, 0)
        screen.clrtoeol()
        screen.addstr(18, 2, "Rolling dice...")
        screen.refresh()
        time.sleep(0.7)

        roll = random.randrange(10000) / 100

        if direction == "u":
            won = roll < threshold
        else:
            won = roll >= threshold

        if won:
            money += profit
            outcome_msg = f"DICE RESULT: {roll:.2f} --> YOU WIN! Profit: +${profit:.2f}"
        else:
            money -= bet
            outcome_msg = f"DICE RESULT: {roll:.2f} --> YOU LOSE! Loss: -${bet:.2f}"

        money = round(money, 2)
        screen.addstr(20, 2, outcome_msg)
        screen.addstr(21, 2, f"New balance: ${money:.2f}")
        screen.refresh()
        time.sleep(1.5)

    for r in range(7, 23):
        screen.move(r, 0)
        screen.clrtoeol()

    if money >= target:
        screen.addstr(10, 2, "CONGRATULATIONS! YOU WIN!")
        screen.addstr(11, 2, f"Final balance: ${money:.2f} (Target: ${target})")
        screen.refresh()
        time.sleep(1.5)
        return True
    else:
        screen.addstr(10, 2, "GAME OVER! YOU WENT BANKRUPT!")
        screen.refresh()
        time.sleep(1.5)
        return False


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
