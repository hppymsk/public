#Conway's Game of Life Simulation

from tkinter import *

class GameOfLife:
    def __init__(self):
        #Options
        self.sleepTime = 100
        self.gridsize = 10

        #Create & Configure root 
        root = Tk()
        root.title('Conway\'s Game of Life')
        root.geometry('500x500')
        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)

        #Create & Configure frame 
        frame=Frame(root)
        frame.grid(row=0, column=0, sticky=N+S+E+W)
        
        #Initialize variables and arrays
        self.isRunning = False
        self.nmatrix = [[0 for y in range(self.gridsize)] for x in range(self.gridsize)] #Neighbor matrix
        self.cellmap = [[0 for y in range(self.gridsize)] for x in range(self.gridsize)] #Cell matrix

        def start():
            if self.buttons[0][0]['state'] == 'disabled':
                for row in range(10):
                    for col in range(10):
                        self.buttons[row][col]['state'] = 'normal'
                self.startbtn.configure(text='START', bg='green')
                self.isRunning = False

            else:
                for row in range(10):
                        for col in range(10):
                            self.buttons[row][col]['state'] = 'disabled'
                self.startbtn.configure(text='STOP', bg='red')
                self.isRunning = True

            while self.isRunning:
                root.update()
                newgeneration()
                root.after(self.sleepTime)

        def pressed(row, col):
            if self.buttons[row][col].cget('bg') == 'white':
                self.buttons[row][col].configure(bg = 'black')
                self.cellmap[row][col] = 1
                addneighbors(row,col)
            else:
                self.buttons[row][col].configure(bg = 'white')
                self.cellmap[row][col] = 0
                delneighbors(row,col)

        def addneighbors(row, col):
            total = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue
                    if row+x < 0 or col+y < 0:
                        continue
                    if row+x >= 10 or col+y >= 10:
                        continue
                    self.nmatrix[x+row][y+col] += 1

        def delneighbors(row, col):
            
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue
                    if row+x < 0 or col+y < 0:
                        continue
                    if row+x >= 10 or col+y >= 10:
                        continue
                    self.nmatrix[x+row][y+col] -= 1

        def newgeneration():
            for x in range(10):
                for y in range(10):
                    if self.cellmap[x][y] == 0 and self.nmatrix[x][y] == 3: #new cell
                        addneighbors(x,y)
                        self.cellmap[x][y] = 1
                        self.buttons[x][y].configure(bg = 'black')

                    if self.cellmap[x][y] == 1:
                        if self.nmatrix[x][y] < 2 or self.nmatrix[x][y] > 3: #cell dies
                            delneighbors(x,y)
                            self.cellmap[x][y] = 0
                            self.buttons[x][y].configure(bg = 'white')
        
        self.startbtn=Button(root, text='START', height=2, width=100, fg='white', bg='green', command=lambda:start())
        self.startbtn.grid(row=1)
        self.buttons = {}

        for row in range(self.gridsize):
            self.buttons[row] = {}
            Grid.rowconfigure(frame, row, weight=1)
            for col in range(self.gridsize):
                Grid.columnconfigure(frame, col, weight=1)
                self.buttons[row][col] = Button(frame, bg = 'white', command = lambda row=row, col=col: pressed(row, col))
                self.buttons[row][col].grid(row=row, column=col, sticky=N+S+E+W)

        root.mainloop()

GameOfLife()