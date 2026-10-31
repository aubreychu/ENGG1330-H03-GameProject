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
    target = random.randint(300, 600)

    screen.addstr(4, 2, "=== MINES GAMBLING PUZZLE ===")
    screen.addstr(5, 2, f"Your target is ${target}! Each round starts with $100.")
    screen.addstr(6, 2, "Find safe tiles to multiply your money. Hit a mine and lose it all!")
    screen.refresh()

    mine_count = 5

    while True:
        money = 100
        mines = random.sample(range(1, 26), mine_count)
        revealed = set()

        while True:
            # Clear dynamic board area (Rows 8 to 22)
            for r in range(8, 23):
                screen.move(r, 0)
                screen.clrtoeol()

            screen.addstr(8, 2, f"--- MINES BOARD | Money: ${money:.2f} | Target: ${target} ---")

            # Draw 5x5 Mines Board on Rows 10 to 14
            for row_idx in range(5):
                line = ""
                for col_idx in range(1, 6):
                    tile_num = row_idx * 5 + col_idx
                    if tile_num in revealed:
                        line += "  O"
                    else:
                        line += f"{tile_num:3}"
                screen.addstr(10 + row_idx, 4, line)

            screen.addstr(16, 2, "Enter 1-25 to reveal a tile, or 0 to cash out.")
            choice = get_input(screen, 18, 2, "Your choice: ")

            if not choice.isdigit():
                screen.addstr(20, 2, "Invalid input!")
                screen.refresh()
                time.sleep(1.0)
                continue

            choice = int(choice)

            if choice == 0:
                screen.addstr(20, 2, f"You cashed out ${money:.2f}!")
                screen.refresh()
                time.sleep(1.2)
                break

            if choice < 1 or choice > 25:
                screen.addstr(20, 2, "Choose a number from 1 to 25.")
                screen.refresh()
                time.sleep(1.0)
                continue

            if choice in revealed:
                screen.addstr(20, 2, "You already picked this tile!")
                screen.refresh()
                time.sleep(1.0)
                continue

            screen.addstr(20, 2, "Revealing tile...")
            screen.refresh()
            time.sleep(0.5)

            if choice in mines:
                screen.addstr(20, 2, "BOOM! You hit a mine!")
                screen.refresh()
                money = 0
                time.sleep(1.2)
                break

            revealed.add(choice)
            money *= 1.25
            screen.addstr(20, 2, f"SAFE! Money increased to ${money:.2f}!")
            screen.refresh()
            time.sleep(0.8)

            if money >= target:
                screen.addstr(21, 2, f"CONGRATULATIONS! YOU WIN! Final: ${money:.2f} / ${target}")
                screen.refresh()
                time.sleep(1.5)
                return True

            if len(revealed) == 25 - mine_count:
                screen.addstr(21, 2, "All safe tiles revealed!")
                screen.refresh()
                time.sleep(1.2)
                break

        again = get_input(screen, 22, 2, "Try another round? (y/n): ").lower()
        if again != "y":
            return False


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
