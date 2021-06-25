#Conway's Game of Life Simulation
#Author: Josh Albertson
#Date: June 23, 2021

#import tkinter
from tkinter import *
import random
import copy
import math

class GameOfLife:
    def __init__(self):
        #Options
        self.isRunning = False
        self.sleepTime = 100
        self.gridsize = 100
        self.canvassize = 800
        self.matrixsize = int(self.canvassize / self.gridsize)
        self.isGridActive = True

        #Create & Configure root and frames
        root = Tk()
        self.canvas = Canvas(root, height=self.canvassize, width=self.canvassize, bg='white')
        self.canvas.pack(fill=BOTH, expand=True)

        self.btnframe = Canvas(root, height=2, width=self.canvassize, bg='white')
        self.btnframe.pack(side=BOTTOM, expand=True)

        def initmatrices():
            self.matrixsize = int(self.canvassize / self.gridsize)
            self.nmatrix = [[0 for y in range(self.matrixsize)] for x in range(self.matrixsize)] #Neighbor matrix
            self.cellmap = [[0 for y in range(self.matrixsize)] for x in range(self.matrixsize)] #Cell matrix
            self.livelist = []
            self.newcell = []

        def getxy(mouseevent):    
            x = math.floor(mouseevent.x / self.gridsize) * self.gridsize
            y = math.floor(mouseevent.y / self.gridsize) * self.gridsize
            xmatrix = int(x / self.gridsize)
            ymatrix = int(y / self.gridsize)
            
            if self.cellmap[xmatrix][ymatrix] == 0:
                self.livelist.append(f'{xmatrix},{ymatrix}')
                addneighbors(xmatrix,ymatrix)
                addsquare(xmatrix, ymatrix)
                #print(self.livelist)
            elif self.cellmap[xmatrix][ymatrix] == 1:
                self.livelist.remove(f'{xmatrix},{ymatrix}')
                deleteneighbors(xmatrix, ymatrix)
                deletesquare(xmatrix, ymatrix)
                #print(self.livelist)
            #print("Position = ({0},{1})".format(x, y))
        
        def addsquare(x, y):
            self.cellmap[x][y] = 1
            if f'{x},{y}' not in self.livelist:
                self.livelist.append(f'{x},{y}')
            x = x * self.gridsize
            y = y * self.gridsize
            print(self.newcell)
            self.canvas.create_rectangle(x+1, y+1, x + self.gridsize-1, y + self.gridsize-1, fill='black', outline='black', tags=f'sq{x}{y}')

        def deletesquare(x, y):
            self.cellmap[x][y] = 0
            #if f'{x},{y}' in self.livelist:
            self.livelist.remove(f'{x},{y}')
            x = x * self.gridsize
            y = y * self.gridsize
            print(self.newcell)
            self.canvas.delete(f'sq{x}{y}')
        
        def start():
            if self.isGridActive:
                create_grid()
            
            """ print('---Cell Map---')
            for x in range(self.matrixsize):
                print(self.cellmap[x])
            print('---Neighbors---')
            for x in range(self.matrixsize):
                print(self.nmatrix[x]) """
            
            if self.isRunning:
                stop()
            else:
                self.startbtn.configure(text='STOP', bg='red')
                self.isRunning = True
            
            while self.isRunning:
                root.update()
                newgeneration()
                #root.update()
                root.after(self.sleepTime)
        
        def stop():
            self.isRunning = False
            self.startbtn.configure(text='START', bg='green')

        def addneighbors(x, y):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: 
                        continue
                    if x+i < 0 or y+j < 0:
                        continue
                    if x+i >= self.matrixsize or y+j >= self.matrixsize:
                        continue
                    self.nmatrix[x+i][y+j] += 1

                    if self.nmatrix[x+i][y+j] == 3:
                        if f'{x+i},{y+j}' in self.newcell:
                            continue
                        else:
                            self.newcell.append(f'{x},{y}')

        def deleteneighbors(x, y):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: 
                        continue
                    if x+i < 0 or y+j < 0:
                        continue
                    if x+i >= self.matrixsize or y+j >= self.matrixsize:
                        continue
                    self.nmatrix[x+i][y+j] -= 1
                    if self.nmatrix[x+i][y+j] != 3:
                        if f'{x+i},{y+j}' in self.newcell:
                            self.newcell.remove(f'{x+i},{y+j}')

        def newgeneration():
            livelistbuffer = copy.deepcopy(self.livelist)
            newcellbuffer = copy.deepcopy(self.newcell)
            nmatrixbuffer = copy.deepcopy(self.nmatrix)

            for i in range(len(livelistbuffer)):
                x = int(livelistbuffer[i].split(',',-1)[0])
                y = int(livelistbuffer[i].split(',',-1)[1])
    
                if nmatrixbuffer[x][y] < 2 or nmatrixbuffer[x][y] > 3: #cell dies
                    self.cellmap[x][y] = 0
                    if f'{x},{y}' in self.livelist:
                        self.livelist.remove(f'{x},{y}')
                    deletesquare(x,y)
                    deleteneighbors(x,y)
            
            for i in range(len(newcellbuffer)):
                x = int(newcellbuffer[i].split(',',-1)[0])
                y = int(newcellbuffer[i].split(',',-1)[1])
                self.cellmap[x][y] = 1
                self.livelist.append(f'{x},{y}')
                addsquare(x,y)
                addneighbors(x,y)
            #print(self.livelist)
            #print(self.newcell)

            """ for x in range(self.matrixsize):
                for y in range(self.matrixsize):
                    if cellmapbuffer[x][y] == 0 and nmatrixbuffer[x][y] == 3: #new cell
                        self.cellmap[x][y] = 1
                        addsquare(x,y)
                        addneighbors(x,y)

                    if cellmapbuffer[x][y] == 1:
                        if nmatrixbuffer[x][y] < 2 or nmatrixbuffer[x][y] > 3: #cell dies
                            self.cellmap[x][y] = 0
                            deletesquare(x,y)
                            deleteneighbors(x,y) """ 


        def randomize():
            for x in range(self.matrixsize):
                for y in range(self.matrixsize):
                    r = random.randint(0,1)
                    if self.cellmap[x][y] == 1:
                        if r == 1:
                            continue
                        else:
                            self.cellmap[x][y] = 0
                            deletesquare(x,y)
                            deleteneighbors(x,y)
                            continue
                    if self.cellmap[x][y] == 0:
                        if r == 0:
                            continue
                        else:
                            self.cellmap[x][y] = 1
                            addsquare(x,y)
                            addneighbors(x,y)
                            continue
            """ print('---Cell Map---')
            for x in range(self.matrixsize):
                print(self.cellmap[x])
            print('---Neighbors---')
            for x in range(self.matrixsize):
                print(self.nmatrix[x]) """

        def reset():
            stop()
            for x in range(self.matrixsize):
                for y in range(self.matrixsize):
                    self.nmatrix[x][y] = 0
                    if self.cellmap[x][y] == 1:
                        self.cellmap[x][y] = 0
                        deletesquare(x,y)
        
        def zoomIn():
            stop()
            reset()
            self.gridsize += 10
            initmatrices()
            if self.isGridActive:
                create_grid()

        def zoomOut():
            if self.gridsize - 10 > 0:
                stop()
                reset()
                self.gridsize -= 10
                initmatrices()
                if self.isGridActive:
                    create_grid()

        def create_grid(event=None):
            #w = c.winfo_width() # Get current width of canvas
            #h = c.winfo_height() # Get current height of canvas
            self.canvas.delete('grid_line') # Will only remove the grid_line

            # Creates all vertical lines at intevals of 100
            for i in range(0, self.canvassize + self.gridsize, self.gridsize):
                self.canvas.create_line([(i, 0), (i, self.canvassize)], tag='grid_line', fill='gray')

            # Creates all horizontal lines at intevals of 100
            for i in range(0, self.canvassize + self.gridsize, self.gridsize):
                self.canvas.create_line([(0, i), (self.canvassize, i)], tag='grid_line', fill='gray')

        self.startbtn=Button(self.btnframe, text='START', height=2, width=25, fg='white', bg='green', command=lambda:start())
        self.resetdbtn=Button(self.btnframe, text='Reset', height=2, width=25, fg='black', bg='yellow', command=lambda:reset())
        self.randbtn=Button(self.btnframe, text='Randomize', height=2, width=25, fg='white', bg='blue', command=lambda:randomize())

        self.plusbtn=Button(self.btnframe, text='+', height=2, width=10, fg='white', bg='gray', command=lambda:zoomIn())
        self.minusbtn=Button(self.btnframe, text='-', height=2, width=10, fg='white', bg='gray', command=lambda:zoomOut())

        self.randbtn.pack(side=LEFT)
        self.resetdbtn.pack(side=LEFT)
        self.startbtn.pack(side=RIGHT)
        self.plusbtn.pack(side=RIGHT)
        self.minusbtn.pack(side=RIGHT)

        self.canvas.bind('<Button-1>', getxy)
        if self.isGridActive:
            create_grid()
        #generateBoard()
        initmatrices()
        root.mainloop()

GameOfLife()