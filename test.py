from tkinter import *
import tkinter
import math

gridsize = 100
canvassize = 800
matrixsize = int(canvassize / gridsize)

nmatrix = [[0 for y in range(matrixsize)] for x in range(matrixsize)] #Neighbor matrix
cellmap = [[0 for y in range(matrixsize)] for x in range(matrixsize)] #Cell matrix

def getxy(event):    
    x = math.floor(event.x / gridsize) * gridsize
    y = math.floor(event.y / gridsize) * gridsize
    xmatrix = x / gridsize
    ymatrix = y / gridsize
    print("Position = ({0},{1})".format(x, y))

def addsquare(x, y):
    c.create_rectangle(x, y, x + gridsize, y + gridsize, fill='black')
def deletesquare(x, y):
    c.create_rectangle(x, y, x + gridsize, y + gridsize, fill='white')

def create_grid(event=None):
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    c.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, gridsize):
        c.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, gridsize):
        c.create_line([(0, i), (w, i)], tag='grid_line')




root = Tk()
c = tkinter.Canvas(root, height=canvassize, width=canvassize, bg='white')
c.pack(fill=tkinter.BOTH, expand=True)
c.bind('<Button-1>', getxy)
c.bind('<Configure>', create_grid)

root.mainloop()