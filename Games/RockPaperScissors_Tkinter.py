""" 
    This is a Tkinter based rock-paper-scissors game.
    Tkinter UI allows choosing desired playing choice (rock/paper/scissors).
    
    Computer choice is randomly chosen in background.
    The playing choices are compared and result in displayed (Player Win / Computer Win / Draw).


    The given program is based on TKinter Rock-Paper-Scissors game created by PythonGeeks Team: 
    https://pythongeeks.org/python-rock-paper-scissors-game/.
"""

import random
import tkinter as tk
from tkinter import *


ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"

PLAYER_WON =   " Player Won "
COMPUTER_WON = "Computer Won"
DRAW =          "    Draw     "

options = [ROCK, PAPER, SCISSORS]

## Mapping of playable combinations -->> key wins againts value
winner_combination_dict = {
    ROCK: SCISSORS,
    PAPER: ROCK,
    SCISSORS: PAPER
}


font_Times_New_Roman = "Times New Roman"


global player_option


class Rock_Paper_Scissors_Game(tk.Tk):

    rounds_count = 0
    user_wins = 0
    computer_wins = 0
    draws = 0


    def __init__(self):
        super().__init__()
        self.title("Rock Paper Scissors Game")
        self.geometry("400x300")
        self.resizable(True, True)
        self.config(bg="#e3f4f1")

        label_font_tuple = (font_Times_New_Roman, 18, 'bold')
        button_font_tuple = (font_Times_New_Roman, 12, 'bold')
        
        self.Label_Player = Label(self, text="PLAYER")
        self.Label_Player.grid(row=1, column=1)
        self.Label_Player.config(bg="#e8c1c7", fg="black", font=label_font_tuple)
        self.Label_Computer = Label(self, text="COMPUTER")
        self.Label_Computer.grid(row=1, column=3)
        self.Label_Computer.config(bg="#e8c1c7", fg="black", font=label_font_tuple)

        self.Label_Player_Pick = Label(self)
        self.Label_Player_Pick.grid(row=2, column=1)
        self.Label_Player_Pick.config(bg="#e8c1c7", fg="black", font=label_font_tuple)
        self.Label_Computer_Pick = Label(self)
        self.Label_Computer_Pick.grid(row=2, column=3)
        self.Label_Computer_Pick.config(bg="#e8c1c7", fg="black", font=label_font_tuple)


        self.Label_Status = Label(self, text="", font=(font_Times_New_Roman, 12))
        self.Label_Status.config(fg="black", font=(font_Times_New_Roman, 12, 'bold','italic'))
        self.Label_Status.grid(row=4, column=2)
        
        
        self.rock = Button(self, text=ROCK, font=button_font_tuple, command=self.Rock) #image=Player_Rock_ado, 
        self.paper = Button(self, text=PAPER, font=button_font_tuple, command=self.Paper) #image=Player_Paper_ado, 
        self.scissor = Button(self, text=SCISSORS, font=button_font_tuple, command=self.Scissor) #image=Player_Scissor_ado, 
        self.button_quit = Button(self, text="Quit", bg="red", fg="white", font=(font_Times_New_Roman, 20, 'bold'), command=self.Exit)
        self.rock.grid(row=5, column=1, pady=30)
        self.paper.grid(row=5, column=2, pady=30)
        self.scissor.grid(row=5, column=3, pady=30)
        self.button_quit.grid(row=6, column=2)


    def Rock(self):
        global player_option
        player_option = ROCK
        self.Label_Player_Pick.config(text=ROCK)
        self.Matching()
    
    def Paper(self):
        global player_option
        player_option = PAPER
        self.Label_Player_Pick.config(text=PAPER)
        self.Matching()
    
    def Scissor(self):
        global player_option
        player_option = SCISSORS
        self.Label_Player_Pick.config(text=SCISSORS)
        self.Matching()



    def Matching(self):

        random_number = random.randint(0, 2)
        # rock: 0, paper: 1, scissors: 2
        computer_pick = options[random_number]
        self.Label_Computer_Pick.config(text=computer_pick)

        if (winner_combination_dict[player_option] == computer_pick):
            self.Label_Status.config(text=PLAYER_WON)
        
        elif (player_option == computer_pick):
            self.Label_Status.config(text=DRAW)
        
        else:
            self.Label_Status.config(text=COMPUTER_WON)
    
    
    def Exit(self):
        exit()

    
if __name__ == "__main__":
    app = Rock_Paper_Scissors_Game()
    app.mainloop()
