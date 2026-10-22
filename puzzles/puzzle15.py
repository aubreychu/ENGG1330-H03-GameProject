#This puzzle will involve the user opening the life jacket locker
import time
import random

def run_puzzle():
    message = "You find yourslef in front of a mysterious locker.\nWhen you approach it you realize it contains life jackets!\nExcited by your discovery you try openeing it only to realize it has remained locked!\nComplete the correct sequence of turns on the dile to access the saftey vest.\nPreform the calculations displayed on screen, if the result is odd turn the knob right otherwise turn it left.\nCareful though, wrong entreis casue the entire sequence to fail at the end forcing you to restart!"
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.05)
    result = False
    sequence = []
    while result == False:
        print("")
        answer =  ""
        result = True
        for i in range(5):
            sequence = [random.randint(1, 10) for _ in range(5)]
            output = ""
            for num in sequence:
                output = output + str(num) + " + "
            sum = 0
            for i in range(len(sequence)):
                sum += sequence[i]
            print(output[:-2])
            answer = input("Enter 'r' for right and 'l' for left: ")
            if sum % 2 == 1:
                if answer != "r":
                    result = False
            else:
                if answer != "l":
                    result = False
        if result == False:
            message = "The sequence wasn't correct!\nTry again!"
            for char in message:
                print(char, end='', flush=True)
                time.sleep(0.05)
    message = "Hurray!!!\nThe locker opens, grab a vest and continue with your escape!"
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.05)
run_puzzle()