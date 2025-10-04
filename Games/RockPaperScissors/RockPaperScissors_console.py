""" 
    This is a simple console based rock-paper-scissors game where user can play againts a computer.
    Computer picks any of the 3 values randomly, and according to the user input, generates the result of each round.
    Once a user decides to quit, the final statistics are shown: 
    total number of rounds played, user's wins, computer's wins, and number of draws.


    This program is based on the program https://github.com/techwithtim/5-Python-Projects-For-Beginners/blob/main/rock_paper_scissors.py
    created by https://github.com/techwithtim/
"""


import random

rounds_count = 0
user_wins = 0
computer_wins = 0
draws = 0

ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

options = [ROCK, PAPER, SCISSORS]

## Mapping of playable combinations -->> key wins againts value
winner_combination_dict = {
    ROCK: SCISSORS,
    PAPER: ROCK,
    SCISSORS: PAPER
}


while True:
    user_input = input("Type Rock/Paper/Scissors to play. Type Q or Quite to quit game. ").lower()
    if user_input == "q" or user_input == "quit":
        break

    if user_input not in options or not user_input:
        print("Please pick a valid playable value (Rock/Paper/Scissors).")
        continue

    else:
        random_number = random.randint(0, 2)
        # rock: 0, paper: 1, scissors: 2
        computer_pick = options[random_number]
        print(f"Computer picked {computer_pick}.")
        
        if (winner_combination_dict[user_input] == computer_pick):
            print("You won!")
            user_wins += 1
        
        elif (user_input == computer_pick):
            print("This round is a draw")
            draws += 1
        
        else:
            print("You lost!")
            computer_wins += 1
        
        rounds_count += 1

print(f"Total number of rounds played: {rounds_count}")
print(f"User win count: {user_wins}.")
print(f"Computer win count: {computer_wins}.")
print(f"Number of draws: {draws}.")

print("Goodbye!")