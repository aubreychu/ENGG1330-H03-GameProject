import os 
os.system('cls')
import random
print("1.The computer randomly generates a 4-digit number with repeated digits.")
print("2.The player has 10 attempts to guess the number.")
print("3.A means a correct digit in the correct position; B means a correct digit in the wrong position.")
print("4.The player wins by guessing all four digits correctly (4A0B).")
print("5.If all attempts are used, the game ends and the secret number is revealed.")  #game rule
answer = "".join(random.choices("0123456789", k=4))  #str
time = 10

while time > 0:
    tryy = input(f"last {time} times ， please input a 4-digit number: ").strip()

    # test
    if len(tryy) != 4 or not tryy.isdigit():
        print("please input a 4-digit number！")
        continue

    A = 0
    B = 0
    answer_list = list(answer)
    guess_list = list(tryy)

    for i in range(4):
        if guess_list[i] == answer_list[i]:
            A += 1
            answer_list[i] = None   # 标记已用
            guess_list[i] = None

    
        if guess_list[i] is not None and guess_list[i] in answer_list:
            B += 1
            answer_list[answer_list.index(guess_list[i])] = None  # 标记已用

    print(f"{A}A{B}B")

    if A == 4:
        print(f"Congragulation, you get it right，the answer is {answer}")
        break

    time -= 1

else:
    print(f"Game over, the answer is {answer}")

    
       
