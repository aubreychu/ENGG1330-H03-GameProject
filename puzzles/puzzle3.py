
import random
import time

def run_puzzle():
    print("=== TREASURE CHEST ===")
    print("Collect 100 gold coins to win!")
    print("Every chest has treasure. No losing!\n")

    gold = 0
    target = 100

    while gold < target:
        print(f"\nGold: {gold}/{target}")
        print("Choose a treasure chest:")
        print("[1] Ancient Chest")
        print("[2] Crystal Chest")
        print("[3] Golden Chest")

        choice = input("Choose (1-3): ").strip()

        if choice not in ["1", "2", "3"]:
            print("Invalid choice!")
            continue

        rewards = [random.randint(10, 30) for _ in range(3)]
        reward = rewards[int(choice) - 1]

        print("\nOpening chest...")
        time.sleep(0.7)
        bomb = random.randrange(1,100)
        if bomb <=20:
            print("Oh no! The chest was trapped! You lost some gold!")
            loss = random.randint(5, 15)
            gold = max(0, gold - loss)
            print(f"-{loss} gold coins!")
        else:
            if reward >= 25:
                print("JACKPOT! A huge treasure!")
            elif reward >= 15:
                print("Nice! You found shiny gold!")
            else:
                print("You found some gold coins!")

        gold += reward
        print(f"+{reward} gold coins!")

    print("\nCONGRATULATIONS!")
    print(f"You collected {gold} gold coins!")
    print("PUZZLE COMPLETED!")
    return True

if __name__ == "__main__":
    run_puzzle()
