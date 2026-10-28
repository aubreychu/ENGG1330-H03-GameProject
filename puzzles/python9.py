import random

print("Pattern Guess")
print("I'll show you a sequence. Guess the next number!")
print("First to get 7 correct wins\n")

rules = [
    ("+2",  lambda x: x + 2),
    ("+3",  lambda x: x + 3),
    ("+5",  lambda x: x + 5),
    ("×2",  lambda x: x * 2),
    ("×3",  lambda x: x * 3),
    ("-1",  lambda x: x - 1),
    ("+10", lambda x: x + 10),
    ("×2+1", lambda x: x * 2 + 1),
]

correct = 0

while correct < 7:
    name, rule = random.choice(rules)
    start = random.randint(1, 10)

    seq = [start]
    for i in range(3):
        seq.append(rule(seq[-1]))

    print(f"Sequence: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ?")
    answer = input("Next number: ").strip()

    if not answer.isdigit():
        print("Please type a number\n")
        continue

    if int(answer) == rule(seq[-1]):
        correct += 1
        print(f"Correct! ({correct}/7)\n")
    else:
        print(f"Wrong! The answer was {rule(seq[-1])}  ({correct}/7)\n")

print("You got 7 correct! You win!")