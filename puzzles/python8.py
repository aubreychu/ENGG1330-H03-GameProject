import os 
os.system('cls')
import random

print("Guess Big or Small")
print("Roll two dice, sum of pips")
print("  Small=2~6   Big=8~12   7=no points")
print("First to win 5 rounds wins the match")

player = 0
computer = 0

while player < 5 and computer < 5:
    player_input = input("big or small: ").strip()

    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    total = d1 + d2
    print(f" {d1} + {d2} = {total}")

    if total == 7:
        print("7 — no points")
    elif (total > 7 and player_input == "big") or (total < 7 and player_input == "small"):
        player += 1
        print(f" You win the round  You {player} : {computer} Computer")
    else:
        computer += 1
        print(f" Computer wins the round  You {player} : {computer} Computer")
    print()

if player == 5:
    print("Congratulations! You win the match!")
else:
    print("Computer wins the match. Better luck next time!")
    