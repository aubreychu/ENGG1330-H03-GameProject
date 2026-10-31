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
    screen.addstr(4, 2, "=== TREASURE CHEST ===")
    screen.addstr(5, 2, "Collect 100 gold coins to win! Every chest has treasure. No losing!")
    screen.refresh()

    gold = 0
    target = 100

    while gold < target:
        for r in range(7, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        screen.addstr(7, 2, f"Gold: {gold}/{target}")
        screen.addstr(8, 2, "Choose a treasure chest:")
        screen.addstr(9, 2, "[1] Ancient Chest")
        screen.addstr(10, 2, "[2] Crystal Chest")
        screen.addstr(11, 2, "[3] Golden Chest")
        screen.refresh()

        choice = get_input(screen, 13, 2, "Choose (1-3): ")

        if choice not in ["1", "2", "3"]:
            screen.addstr(15, 2, "Invalid choice!")
            screen.refresh()
            time.sleep(0.8)
            continue

        rewards = [random.randint(10, 30) for _ in range(3)]
        reward = rewards[int(choice) - 1]

        screen.addstr(15, 2, "Opening chest...")
        screen.refresh()
        time.sleep(0.7)

        bomb = random.randrange(1, 100)
        if bomb <= 20:
            loss = random.randint(5, 15)
            gold = max(0, gold - loss)
            screen.addstr(17, 2, "Oh no! The chest was trapped! You lost some gold!")
            screen.addstr(18, 2, f"-{loss} gold coins!")
        else:
            if reward >= 25:
                screen.addstr(17, 2, "JACKPOT! A huge treasure!")
            elif reward >= 15:
                screen.addstr(17, 2, "Nice! You found shiny gold!")
            else:
                screen.addstr(17, 2, "You found some gold coins!")

        gold += reward
        screen.addstr(19, 2, f"+{reward} gold coins!")
        screen.refresh()
        time.sleep(1.2)

    screen.addstr(21, 2, f"CONGRATULATIONS! You collected {gold} gold coins! PUZZLE COMPLETED!")
    screen.refresh()
    time.sleep(1.5)
    return True


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
