""" 
    This is a Tkinter based 2048 game.
    Tkinter UI shows the color coded numbered tiles and current score.

    This program is based on the code shared by Rahul Patodi in his post https://projectsflood.com/how-i-turned-an-idea-into-the-2048-game-f600ef57bd1f 
    in the Medium Publication https://projectsflood.com.
"""



from tkinter import messagebox, Tk, Label, Frame
import random


## Helper Constants

GAME_2048 = "2048 Game"
RETURN_KEY = "Return"
RESTART_GAME_MESSAGE = "Press Enter to restart."


## Helper Functions

### Gets the current score to be shown on the game UI window
def getScore(score):
    return f"Score: {score}"

### Initialises / Resets the grid into empty 4 x 4 cells
def createEmptyGridCell():
    return [[0]*4 for _ in range(4)]


class Board:
    def __init__(self):
        self.window = Tk()
        self.window.title(GAME_2048)
        
        self.score = 0
        self.score_label = Label(self.window, text = getScore(self.score), font=('arial', 24, 'bold'))
        self.score_label.pack()
        
        self.gameArea = Frame(self.window, bg='azure3')
        self.board = []
        self.gridCell = createEmptyGridCell() #[[0]*4 for _ in range(4)]
        self.create_grid()
        self.gameArea.pack()
        
        self.compress = False
        self.merge = False
        self.moved = False


    def create_grid(self):
        for i in range(4):
            row = []
            for j in range(4):
                label = Label(self.gameArea, text='', bg='azure4', font=('arial', 22, 'bold'), width=4, height=2)
                label.grid(row=i, column=j, padx=7, pady=7)
                row.append(label)
            self.board.append(row)
    
    def reset(self):
        self.gridCell = createEmptyGridCell()  #[[0]*4 for _ in range(4)]
        self.score = 0
        self.update_score()
        self.paint_grid()
        
    def update_score(self):
        self.score_label.config(text = getScore(self.score))

    def reverse(self):
        for i in range(4):
            self.gridCell[i] = self.gridCell[i][::-1]
    
    def transpose(self):
        self.gridCell = [list(row) for row in zip(*self.gridCell)]
    
    def compress_grid(self):
        self.compress = False
        new_grid = createEmptyGridCell()  #[[0]*4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if self.gridCell[i][j] != 0:
                    new_grid[i][pos] = self.gridCell[i][j]
                    if pos != j:
                        self.compress = True
                    pos += 1
        self.gridCell = new_grid
    
    def merge_grid(self):
        self.merge = False
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j+1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True
        self.update_score()
    
    def random_cell(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.gridCell[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.gridCell[i][j] = 2
    
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
        for i in range(3):
            for j in range(4):
                if self.gridCell[i+1][j] == self.gridCell[i][j]:
                    return True
        return False
    

    ## Define tile colors corresponding to each number
    def paint_grid(self):
        bg_color = {
            '2': '#eee4da',
            '4': '#ede0c8',
            '8': '#f2b179',
            '16': '#f59563',
            '32': '#f67c5f',
            '64': '#f65e3b',
            '128': '#edcf72',
            '256': '#edcc61',
            '512': '#edc850',
            '1024': '#edc53f',
            '2048': '#edc22e',
        }
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    self.board[i][j].config(text='', bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]), bg=bg_color.get(str(self.gridCell[i][j]),
                                                                                            'black'))


class Game:
    def __init__(self, gameboard):
        self.board = gameboard
        self.end = False
        self.won = False


    def start(self):
        self.board.reset()
        self.board.random_cell()
        self.board.random_cell()
        self.board.paint_grid()
        self.board.window.bind('<Key>', self.link_keys)
        self.board.window.mainloop()
    
    def restart_game(self, event):
        if event.keysym == RETURN_KEY:
            self.end = False
            self.won = False
            self.start()
    
    def link_keys(self, event):
        if self.end or self.won:
            if event.keysym == RETURN_KEY:
                self.restart_game(event)
            return


        self.board.compress = False
        self.board.merge = False
        self.board.moved = False
        
        key = event.keysym
        
        if key == 'Up':
            self.board.transpose()
            self.board.compress_grid()
            self.board.merge_grid()
            self.board.moved = self.board.compress or self.board.merge
            self.board.compress_grid()
            self.board.transpose()
        
        elif key == 'Down':
            self.board.transpose()
            self.board.reverse()
            self.board.compress_grid()
            self.board.merge_grid()
            self.board.moved = self.board.compress or self.board.merge
            self.board.compress_grid()
            self.board.reverse()
            self.board.transpose()
        
        elif key == 'Left':
            self.board.compress_grid()
            self.board.merge_grid()
            self.board.moved = self.board.compress or self.board.merge
            self.board.compress_grid()
        
        elif key == 'Right':
            self.board.reverse()
            self.board.compress_grid()
            self.board.merge_grid()
            self.board.moved = self.board.compress or self.board.merge
            self.board.compress_grid()
            self.board.reverse()


        self.board.paint_grid()
        
        if any(2048 in row for row in self.board.gridCell):
            self.won = True
            messagebox.showinfo(GAME_2048, f'You Won!! {RESTART_GAME_MESSAGE}')
            return
        
        if not any(0 in row for row in self.board.gridCell) and not self.board.can_merge():
            self.end = True
            messagebox.showinfo(GAME_2048, f'Game Over!!! {RESTART_GAME_MESSAGE}')
        
        if self.board.moved:
            self.board.random_cell()
        
        self.board.paint_grid()



if __name__ == "__main__":
    board = Board()
    game = Game(board)
    game.start()
