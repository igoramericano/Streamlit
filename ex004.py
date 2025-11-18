from random import *

npc = randint(0, 101)

while True:
    try:
        player = int(input('Try to guess between 0 and 100: '))
    except ValueError:
        print('Invalid input! Please enter an INTEGER number between 0 and 100.')
        continue
    if player == npc:
        print('Congratulations! You guessed it right!')
        break
    elif player < 0 or player > 100:
        print('Out of bounds! Please try again (between 0 and 100).')
    elif player < npc:
        print('Too low, try again!')
    elif player > npc:
        print('Too high, try again!')