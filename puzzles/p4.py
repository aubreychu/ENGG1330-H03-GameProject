import random
import time

def run_puzzle():
    print("=== SLOT MACHINE ===")
    money = 100
    target = random.randint(150, 250)
    spins = 10
    symbols = ["🍒", "🍋", "🍇", "🔔", "💎", "7️⃣"]

    print(f"Target: ${target}")
    print("You have 10 spins. Each spin costs $10.")
    print("3 matches: +$100 | 2 matches: +$30\n")

    while money >= 10 and money < target and spins > 0:
        print(f"\nBalance: ${money} / ${target}")
        print(f"Spins remaining: {spins}")
        input("Press ENTER to spin: ")

        money -= 10
        spins -= 1
        print("Spinning...")
        time.sleep(0.7)

        reels = random.choices(symbols, k=3)
        print(" | ".join(reels))

        if len(set(reels)) == 1:
            money += 100
            print("JACKPOT! +$100!")
        elif len(set(reels)) == 2:
            money += 30
            print("Two matches! +$30!")
        else:
            print("No match! -$10!")

    if money >= target:
        print(f"\nYOU WIN! Final balance: ${money}")
        return True
    else:
        print(f"\nGAME OVER! Final balance: ${money}")
        return False

if __name__ == "__main__":
    run_puzzle()