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

def type_text(screen, row, col, text, delay=0.02):
    """Draws text with a typewriter effect within 80x24 bounds."""
    r = row
    screen.move(r, col)
    for char in text:
        if char == "\n":
            r += 1
            if r < 23:
                screen.move(r, col)
        else:
            if r < 23:
                screen.addstr(char)
                screen.refresh()
                time.sleep(delay)

def run_puzzle(screen):
    curses.curs_set(0)
    money = 100
    target = random.randint(150, 250)
    spins = 10
    symbols = ["🍒", "🍋", "🍇", "🔔"]

    screen.addstr(4, 2, "=== SLOT MACHINE ===")
    type_text(screen, 5, 2, f"Target: ${target} | You entered the arcade. You have 10 spins. Each spin costs $10.")
    type_text(screen, 6, 2, "3 matches: +$100 | 2 matches: +$45")
    screen.refresh()

    while money >= 10 and money < target and spins > 0:
        for r in range(8, 23):
            screen.move(r, 0)
            screen.clrtoeol()

        screen.addstr(8, 2, f"Balance: ${money} / ${target}   |   Spins remaining: {spins}")
        get_input(screen, 10, 2, "Press ENTER to spin: ", max_len=1)

        money -= 10
        spins -= 1
        type_text(screen, 12, 2, "Spinning...")
        screen.refresh()
        time.sleep(0.7)

        reels = random.choices(symbols, k=3)
        type_text(screen, 14, 4, " | ".join(reels))

        if len(set(reels)) == 1:
            money += 100
            screen.addstr(16, 2, "JACKPOT! +$100!")
        elif len(set(reels)) == 2:
            money += 45
            screen.addstr(16, 2, "Two matches! +$45!")
        else:
            screen.addstr(16, 2, "No match! -$10!")

        screen.refresh()
        time.sleep(1.2)

    if money >= target:
        type_text(screen, 19, 2, f"YOU WIN! Final balance: ${money}")
        screen.refresh()
        time.sleep(1.5)
        return True
    else:
        type_text(screen, 19, 2, f"GAME OVER! Final balance: ${money}")
        screen.refresh()
        time.sleep(1.5)
        return False


if __name__ == "__main__":
    curses.wrapper(run_puzzle)
