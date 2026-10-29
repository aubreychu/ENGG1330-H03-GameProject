
import random
import time
import sys

def run_puzzle():
    print("=== MINES GAMBLING PUZZLE ===")

    target = random.randint(300, 600)
    print(f"\nYour target is ${target}!")
    print("Each round starts with $100.")
    print("Find safe tiles to multiply your money.")
    print("Hit a mine and you lose everything!")

    money = 100
    size = 5
    mine_count = 5

    while True:
        mines = random.sample(range(1, 26), mine_count)
        revealed = set()

        print("\n--- NEW ROUND ---")
        print(f"Money: ${money:.2f}")
        print(f"Target: ${target}")

        while True:
            print("\n    MINES BOARD")
            for i in range(1, 26):
                if i in revealed:
                    print("  O", end="")
                else:
                    print(f"{i:3}", end="")

                if i % 5 == 0:
                    print()

            print(f"\nCurrent money: ${money:.2f}")
            print(f"\nTarget: ${target}")
            print("Enter 1-25 to reveal a tile.")
            print("Enter 0 to cash out.")

            choice = input("Your choice: ").strip()

            if not choice.isdigit():
                print("Invalid input!")
                continue

            choice = int(choice)

            if choice == 0:
                print(f"\nYou cashed out ${money:.2f}!")
                break

            if choice < 1 or choice > 25:
                print("Choose a number from 1 to 25.")
                continue

            if choice in revealed:
                print("You already picked this tile!")
                continue

            print("Revealing tile...")
            time.sleep(0.5)

            if choice in mines:
                print("\nBOOM! You hit a mine!")
                money = 0
                break

            revealed.add(choice)

            money *= 1.25
            print(f"SAFE! Money increased to ${money:.2f}!")

            if money >= target:
                print("\n" + "=" * 30)
                print("CONGRATULATIONS! YOU WIN!")
                print(f"Final money: ${money:.2f}")
                print(f"Target: ${target}")
                print("=" * 30)
                return True

            if len(revealed) == 25 - mine_count:
                print("All safe tiles revealed!")
                break

        again = input("\nTry another round? (y/n): ").lower()
        if again != "y":
            print("Game over!")
            return False


if __name__ == "__main__":
    run_puzzle()