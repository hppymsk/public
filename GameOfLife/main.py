#Conway's Game of Life Simulation

from tkinter import *
import random
import copy

class GameOfLife:
    def __init__(self):
        #Options
        self.sleepTime = 50
        self.gridsize = 30

        #Create & Configure root 
        root = Tk()
        root.title('Conway\'s Game of Life')
        root.geometry('800x800')
        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)

        #Create & Configure frame 
        btnframe=Frame(root)
        btnframe.grid(row=1, column=0, sticky=N+S+E+W)
        #Grid.rowconfigure(btnframe, 0, weight=1)
        #Grid.columnconfigure(btnframe, 0, weight=1)

        self.isRunning = False

        #self.nmatrix = [[0 for y in range(self.gridsize)] for x in range(self.gridsize)] #Neighbor matrix
        #self.cellmap = [[0 for y in range(self.gridsize)] for x in range(self.gridsize)] #Cell matrix

        def start():
            if self.isRunning:
                stop()
            else:
                for row in range(self.gridsize):
                        for col in range(self.gridsize):
                            self.buttons[row][col]['state'] = 'disabled'
                self.startbtn.configure(text='STOP', bg='red')
                self.isRunning = True
            #newgeneration()
            while self.isRunning:
                root.update()
                newgeneration()
                root.after(self.sleepTime)
        def stop():
            self.isRunning = False
            self.startbtn.configure(text='START', bg='green')
            for row in range(self.gridsize):
                    for col in range(self.gridsize):
                        self.buttons[row][col]['state'] = 'normal'

        def pressed(row, col):
            if self.cellmap[row][col] == 0:
                self.buttons[row][col].configure(bg = 'black')
                self.cellmap[row][col] = 1
                addneighbors(row,col)
            else:
                self.buttons[row][col].configure(bg = 'white')
                self.cellmap[row][col] = 0
                delneighbors(row,col)

        def addneighbors(row, col):
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0: 
                        continue
                    if row+x < 0 or col+y < 0:
                        continue
                    if row+x >= self.gridsize or col+y >= self.gridsize:
                        continue
                    self.nmatrix[x+row][y+col] += 1

        def delneighbors(row, col):
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue
                    if row+x < 0 or col+y < 0:
                        continue
                    if row+x >= self.gridsize or col+y >= self.gridsize:
                        continue
                    self.nmatrix[x+row][y+col] -= 1

        def newgeneration():
            cellmapbuffer = copy.deepcopy(self.cellmap)
            nmatrixbuffer = copy.deepcopy(self.nmatrix)

            for x in range(self.gridsize):
                for y in range(self.gridsize):
                    if cellmapbuffer[x][y] == 0 and nmatrixbuffer[x][y] == 3: #new cell
                        addneighbors(x,y)
                        self.cellmap[x][y] = 1
                        self.buttons[x][y].configure(bg = 'black')

                    if cellmapbuffer[x][y] == 1:
                        if nmatrixbuffer[x][y] < 2 or nmatrixbuffer[x][y] > 3: #cell dies
                            delneighbors(x,y)
                            self.cellmap[x][y] = 0
                            self.buttons[x][y].configure(bg = 'white')

        def randomize():
            for x in range(self.gridsize):
                for y in range(self.gridsize):
                    r = random.randint(0,1)
                    if self.cellmap[x][y] == 1:
                        if r == 1:
                            continue
                        else:
                            self.cellmap[x][y] = 0
                            self.buttons[x][y].configure(bg = 'white')
                            delneighbors(x,y)
                            continue
                    if self.cellmap[x][y] == 0:
                        if r == 0:
                            continue
                        else:
                            self.cellmap[x][y] = 1
                            self.buttons[x][y].configure(bg = 'black')
                            addneighbors(x,y)
                            continue
            """ print('---Cell Map---')
            for x in range(self.gridsize):
                print(self.cellmap[x])
            print('---Neighbors---')
            for x in range(self.gridsize):
                print(self.nmatrix[x]) """

        def reset():
            stop()
            for x in range(self.gridsize):
                for y in range(self.gridsize):
                    self.nmatrix[x][y] = 0
                    self.cellmap[x][y] = 0
                    self.buttons[x][y].configure(bg = 'white')
        def increaseBoardSize():
            stop()
            self.frame.destroy()
            self.gridsize += 10
            generateBoard()

        def decreaseBoardSize():
            stop()
            self.frame.destroy()
            self.gridsize -= 10
            generateBoard()

        def generateBoard():
            self.buttons = {}
            self.nmatrix = [[0 for y in range(self.gridsize)] for x in range(self.gridsize)] #Neighbor matrix
            self.cellmap = [[0 for y in range(self.gridsize)] for x in range(self.gridsize)] #Cell status matrix
            self.frame=Frame(root)
            self.frame.grid(row=0, column=0, sticky=N+S+E+W)
            for row in range(self.gridsize):
                self.buttons[row] = {}
                Grid.rowconfigure(self.frame, row, weight=1)
                for col in range(self.gridsize):
                    Grid.columnconfigure(self.frame, col, weight=1)
                    self.buttons[row][col] = Button(self.frame, bg = 'white', command = lambda row=row, col=col: pressed(row, col))
                    self.buttons[row][col].grid(row=row, column=col, sticky=N+S+E+W)

        self.startbtn=Button(btnframe, text='START', height=2, width=25, fg='white', bg='green', command=lambda:start())
        self.resetdbtn=Button(btnframe, text='Reset', height=2, width=25, fg='black', bg='yellow', command=lambda:reset())
        self.randbtn=Button(btnframe, text='Randomize', height=2, width=25, fg='white', bg='blue', command=lambda:randomize())

        self.plusbtn=Button(btnframe, text='+', height=2, width=10, fg='white', bg='gray', command=lambda:increaseBoardSize())
        self.minusbtn=Button(btnframe, text='-', height=2, width=10, fg='white', bg='gray', command=lambda:decreaseBoardSize())

        self.randbtn.pack(side=LEFT)
        self.resetdbtn.pack(side=LEFT)
        self.startbtn.pack(side=RIGHT)
        self.plusbtn.pack(side=RIGHT)
        self.minusbtn.pack(side=RIGHT)

        generateBoard()

        root.mainloop()

GameOfLife()