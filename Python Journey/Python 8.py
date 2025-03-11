import random
#in exercise we gonna try to generate random number

number = random.randint(1, 6) # this is to generate integer from 1-6
number1 = random.random() #to generate random floats from 0-1

low = 1
high = 100
number2 = random.randint(low, high) # this is to generate integer from low-high

#to pick random choice from a collect e.g a tuple
options = ("rock","paper","scissors")
number3 = random.choice(options)

#trying to shuffle a deck of cards 
cards = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
random.shuffle(cards)
print()
print(number3)
print(cards)


# We are going create a random number guessing game
"""lowest_num = 1
highest_num = 100
answer = random.randint(lowest_num, highest_num)
guesses = 0
is_running = True



print("Python number guessing game")
print(f"Select a number between {lowest_num} and {highest_num}")

while is_running:
    guess = input("Enter your guess: ")
    if guess.isdigit():
        guess = int(guess)
        guesses = guesses + 1
        if guess < lowest_num or guess > highest_num:
            print("That number is out of range")
            print(f"Select a number between {lowest_num} and {highest_num}")
        elif guess < answer:
            print("Too low! try again!")
        elif guess > answer:
            print("Too high! try again!")
        else:
            print(f"CORRECT!!! THE ANSWER IS {answer}")
            print(f"You guessed {guesses} times")
            is_running =False
    else:
        print("invalid guess")
        print(f"Select a number between {lowest_num} and {highest_num}")"""



#This is a rock paper scissors program
"""Game_option = ("rock","paper","scissor")
player = ""
#computer = random.choice(Game_option)
playing = True

while playing:
    computer = random.choice(Game_option)
    while player not in Game_option:
        player = input("Enter either(rock, paper or scissor): ")

    print(f"You picked {player}")
    print(f"Computer picked {computer}")
    if player == computer:
        print("Its a tie!!")
    elif player == "rock" and computer == "scissor":
        print("You win!!")
    elif player == "scissor" and computer == "paper":
        print("You win!!")
    elif player == "paper" and computer == "rock":
        print("You win!!")
    else:
        print("You lose!!")
    
    still_playing = input("Do you wonna play again? (Yes/No), Enter[y/n]: ").lower()
    if not still_playing  == "y" and not still_playing == "n":
        print(f"{still_playing} is not (y) or (n)")
    elif still_playing == "y":
        playing = True
        player = input("Enter either(rock, paper or scissor): ")
    elif still_playing == "n":
        playing = False

print("thanks for playing")"""




#We are going to create a program for rolling a dice
#print("\u25CF \u250C \u2500 \u2510 \u2502 \u2514 \u2518")

# ● ┌ ─ ┐ │ └ ┘

"""  "┌─────────┐"
     "│         │"
     "│         │"
     "│         │"
     "└─────────┘" """


dice_art = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"),
    2: ("┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"),
    3: ("┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘")
}

dice = []
total = 0
num_of_dice = int(input("How many times to role the dice ?: "))

for dic in range(num_of_dice):
    random_num = random.randint(1,6)
    dice.append(random_num)

for dic in range(num_of_dice):
    for line in dice_art.get(dice[dic]):
        print(line)
print()

print("HORIZONTAL VIEW BELOW")
#this is to arrange the dice horizontally

"""if num_of_dice <= 5:
    if num_of_dice == 1:
        completion_num = 4
    elif num_of_dice == 2:
        completion_num = 3
    elif num_of_dice == 3:
        completion_num = 2
    elif num_of_dice == 4:
        completion_num = 1
    elif num_of_dice == 5:
        completion_num = 0
else:
    completion_num = 0"""

completion_num = 5 #because each dice art is drawn on five lines
for line in range(completion_num): #it needs to iterate five times to draw each dice art
    for dic in dice:
        print(dice_art.get(dic)[line], end=" ")
    print()

for dic in dice:
    total += dic
print(f"total: {total}")