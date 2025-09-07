""" 
    This is a simple console based quiz game providing hard coded questions and hard coded answers.
    The results for each question (correct / incorrect) and final score are all displayed in the console.


    This program is based on the program https://github.com/techwithtim/5-Python-Projects-For-Beginners/blob/main/quiz_game.py
    created by https://github.com/techwithtim/
"""


print("Welcome to quiz game!")

playing = input("Would you like to play? ")

if playing.lower() != "yes":
    quit()

print("Okay! Let's play :)")
score = 0

CORRECT = "Correct!"
INCORRECT = "Incorrect!"

answer = input("What does CPU stand for? ")
if answer.lower() == "central processing unit":
    print(CORRECT)
    score += 1
else:
    print(INCORRECT)

answer = input("What does GPU stand for? ")
if answer.lower() == "graphics processing unit":
    print(CORRECT)
    score += 1
else:
    print(INCORRECT)

answer = input("What does RAM stand for? ")
if answer.lower() == "random access memory":
    print(CORRECT)
    score += 1
else:
    print(INCORRECT)

answer = input("What does PSU stand for? ")
if answer.lower() == "power supply unit":
    print(CORRECT)
    score += 1
else:
    print(INCORRECT)

print("You got " + str(score) + " questions correct!")
print("Your score is " + str((score / 4) * 100) + "")