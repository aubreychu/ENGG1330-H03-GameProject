
import random
import time

def run_puzzle():
    print("=== STAKE DICE PUZZLE ===")

    money = 100.0
    target = random.randint(300, 600)

    print(f"\nStarting balance: ${money:.2f}")
    print(f"Target: ${target}")
    print("Reach the target without going bankrupt!")
    print("Dice range: 0.00 - 99.99")
    print("House edge: 1%")

    round_number = 0

    while money > 0 and money < target:
        round_number += 1

        print("\n" + "=" * 40)
        print(f"ROUND {round_number}")
        print(f"Balance: ${money:.2f}")
        print(f"Target: ${target}")
        print("=" * 40)

        # Choose bet amount
        while True:
            try:
                bet = float(input("\nEnter bet amount: $"))

                if 0 < bet <= money:
                    break

                print("Invalid bet amount!")

            except ValueError:
                print("Please enter a valid number.")

        # Choose dice threshold
        while True:
            try:
                threshold = float(
                    input("Enter dice threshold (2-98): ")
                )

                if 2 <= threshold <= 98:
                    break

                print("Threshold must be between 2 and 98!")

            except ValueError:
                print("Please enter a valid number.")

        # Calculate Over and Under payouts
        # Round to 2 decimal places to match dice precision
        threshold = round(threshold, 2)

        under_chance = threshold
        over_chance = 100 - threshold

        under_multiplier = 99 / under_chance
        over_multiplier = 99 / over_chance

        under_profit = bet * (under_multiplier - 1)
        over_profit = bet * (over_multiplier - 1)

        print("\n" + "-" * 40)
        print("AVAILABLE BETS")
        print("-" * 40)

        print(f"\n[U] UNDER {threshold:.2f}")
        print(f"Win chance: {under_chance:.2f}%")
        print(f"Multiplier: {under_multiplier:.4f}x")
        print(f"Potential profit: +${under_profit:.2f}")

        print(f"\n[O] OVER {threshold:.2f}")
        print(f"Win chance: {over_chance:.2f}%")
        print(f"Multiplier: {over_multiplier:.4f}x")
        print(f"Potential profit: +${over_profit:.2f}")

        # Choose roll direction
        while True:
            direction = input(
                "\nRoll [O]ver or [U]nder? "
            ).strip().lower()

            if direction in ["o", "u"]:
                break

            print("Invalid choice!")

        if direction == "u":
            multiplier = under_multiplier
            profit = under_profit
            print(f"\nYou chose UNDER {threshold:.2f}")
        else:
            multiplier = over_multiplier
            profit = over_profit
            print(f"\nYou chose OVER {threshold:.2f}")

        print(f"Bet: ${bet:.2f}")
        print(f"Potential profit: +${profit:.2f}")

        input("\nPress ENTER to roll...")

        print("Rolling dice...")
        time.sleep(0.7)

        # Generate dice roll from 0.00 to 99.99
        roll = random.randrange(10000) / 100

        print(f"\nDICE RESULT: {roll:.2f}")

        # Determine outcome
        if direction == "u":
            won = roll < threshold
        else:
            won = roll >= threshold

        if won:
            money += profit

            print("\nYOU WIN!")
            print(f"Profit: +${profit:.2f}")

        else:
            money -= bet

            print("\nYOU LOSE!")
            print(f"Loss: -${bet:.2f}")

        money = round(money, 2)

        print(f"\nNew balance: ${money:.2f}")

    print("\n" + "=" * 40)

    if money >= target:
        print("CONGRATULATIONS! YOU WIN!")
        print(f"Final balance: ${money:.2f}")
        print(f"Target: ${target}")
        return True

    else:
        print("GAME OVER! YOU WENT BANKRUPT!")
        return False


if __name__ == "__main__":
    run_puzzle()
