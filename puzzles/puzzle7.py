import os 
os.system('cls')
import random
#game rule
print("Welcome to NUMBER BOMB!\nA secret bomb number is hidden in a range (e.g. 0-99).\nPlayers take turns guessing a number.")
print("After each guess, the range shrinks:")
print("   ","- Too low  -> everything up to your guess is eliminated")
print("   ","- Too high -> everything from your guess upward is eliminated")
print("The player forced to guess the BOMB number loses!\nLast one standing wins. Good luck!")

#randomize
x=random.randint(0,100)
times=10

while times>0:
    y=int(input())
    if y>x:
        print("Guess it smaller")
        times-=1
    elif y<x:
        print("Guess it higher")
        times-=1
    else:
        print("Congradulation! You get it right")
    