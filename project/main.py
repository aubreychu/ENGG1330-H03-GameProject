import curses
import random
import time

from title_screen import run_title_screen
from puzzles import (
    puzzle1,
    puzzle2,
    puzzle3,
    puzzle4,
    puzzle5,
    puzzle6,
    puzzle7,
    puzzle8,
    puzzle9,
    puzzle10,
    puzzle11,
    puzzle12,
    puzzle13,
    puzzle14,
    puzzle15,
)

BASE_ROOM_TIME = 60

CATALOG = [
    {"name": "Mines Board", "run": puzzle1.run_puzzle},
    {"name": "Stake Dice", "run": puzzle2.run_puzzle},
    {"name": "Treasure Chest", "run": puzzle3.run_puzzle},
    {"name": "Slot Machine", "run": puzzle4.run_puzzle},
    {"name": "Chill Session", "run": puzzle5.run_puzzle},
    {"name": "4-Digit Code", "run": puzzle6.run_puzzle},
    {"name": "Number Bomb", "run": puzzle7.run_puzzle},
    {"name": "Big or Small Dice", "run": puzzle8.run_puzzle},
    {"name": "Pattern Guess", "run": puzzle9.run_puzzle},
    {"name": "Nim (15 Sticks)", "run": puzzle10.run_puzzle},
    {"name": "Locked Door", "run": puzzle11.run_puzzle},
    {"name": "Leaking Pipe", "run": puzzle12.run_puzzle},
    {"name": "Dark Storage Room", "run": puzzle13.run_puzzle},
    {"name": "Five Identical Doors", "run": puzzle14.run_puzzle},
    {"name": "Life Jacket Locker", "run": puzzle15.run_puzzle},
]


def generate_rooms(catalog, num_rooms=6):
    return random.sample(catalog, k=num_rooms)


def show_help_screen(screen):
    """Displays the How to Play instructions within the 80x24 terminal."""
    screen.timeout(-1)
    screen.erase()
    screen.addstr(2, 2, "=== TITANIC ESCAPE | HOW TO PLAY ===")
    screen.addstr(3, 2, "-" * 70)
    screen.addstr(5, 2, "The RMS Titanic has struck an iceberg and is rapidly taking on water!")
    screen.addstr(7, 2, "OBJECTIVE:")
    screen.addstr(8, 4, "- Ascend through 6 randomized compartments to reach the Boat Deck.")
    screen.addstr(9, 4, "- Solve the puzzle in each room to unlock the way forward.")
    screen.addstr(11, 2, "CONTROLS:")
    screen.addstr(12, 4, "- Follow the on-screen prompts in each room.")
    screen.addstr(13, 4, "- Type your answer and press [ENTER] to submit.")
    screen.addstr(15, 2, "WIN / LOSS:")
    screen.addstr(16, 4, "- Clear all 6 rooms to board a lifeboat and survive!")
    screen.addstr(17, 4, "- Failing a room will cause the ship to sink (Game Over).")
    screen.addstr(20, 2, "Press any key to return to the Title Screen...")
    screen.refresh()
    screen.get_wch()


def play_game(screen):
    curses.curs_set(0)

    # Title screen menu loop
    while True:
        choice = run_title_screen(screen)
        # Restore blocking input mode after title screen's 100ms animation timeout
        screen.timeout(-1)

        if choice == "q":
            return False
        elif choice == "h":
            show_help_screen(screen)
        elif choice == "c":
            break

    run = generate_rooms(CATALOG, num_rooms=6)
    carried_over_time = 0.0
    
    for n, room in enumerate(run, start=1):
        screen.erase()
        allowed_time = BASE_ROOM_TIME + carried_over_time
        # Draw a fixed header at Row 0 to Row 2
        screen.addstr(0, 2, f"=== TITANIC ESCAPE | Room {n} of {len(run)} ===")
        screen.addstr(1, 2, f"Location: {room['name']}")
        screen.addstr(2, 2, "-" * 70)
        screen.refresh()

        # Call the puzzle
        start_time = time.time()
        passed = room["run"](screen)
        elapsed = time.time() - start_time
        screen.timeout(-1)

        # Loss Condition 1: Exceeded the room's time limit
        if elapsed > allowed_time:
            screen.erase()
            screen.addstr(9, 20, "========================================")
            screen.addstr(10, 20, "  TIME EXPIRED! The deck has flooded!   ")
            screen.addstr(11, 20, "========================================")
            screen.addstr(13, 20, f"Allowed: {int(allowed_time)}s | Time Taken: {int(elapsed)}s")
            screen.addstr(14, 20, "The ship sinks and you go down with it...")
            screen.addstr(17, 20, "Press any key to exit...")
            screen.refresh()
            screen.get_wch()
            return False
        # Loss Condition 2: Puzzle failure
        if not passed:
            screen.erase()
            screen.addstr(10, 25, "GAME OVER! You failed the puzzle.")
            screen.addstr(12, 25, "Press any key to exit...")
            screen.refresh()
            screen.get_wch()
            return False
        surplus = allowed_time - elapsed
        carried_over_time = surplus
        
        if n < len(run):
            screen.erase()
            screen.addstr(9, 20, "========================================")
            screen.addstr(10, 20, f"  COMPARTMENT {n} CLEARED! ({int(elapsed)}s spent)  ")
            screen.addstr(11, 20, "========================================")
            screen.addstr(13, 20, f"+{int(surplus)}s bonus carried to the next deck!")
            screen.addstr(15, 20, "Ascending to the next level...")
            screen.addstr(17, 20, "Press any key to continue...")
            screen.refresh()
            screen.get_wch()

    # Victory screen
    screen.erase()
    screen.addstr(9, 18, "********************************************")
    screen.addstr(10, 18, "  VICTORY! You reached the Boat Deck!       ")
    screen.addstr(11, 18, "********************************************")
    screen.addstr(13, 18, f"You successfully launched a lifeboat!")
    screen.addstr(14, 18, f"Remaining time banked: {int(carried_over_time)} seconds.")
    screen.addstr(17, 18, "Press any key to exit...")
    screen.refresh()
    screen.get_wch()
    return True


if __name__ == "__main__":
    curses.wrapper(play_game)

