from mazelib.generate.Prims import Prims
from mazelib.generate.Kruskal import Kruskal
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import torch
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import collections
import numpy as np
import tkinter as tk

# set seed for numpy shuffle
np.random.seed(2)

size_rectangle= 15

side_length_square = 31
height = side_length_square
width = side_length_square
assert height%2 == 1 and width%2==1, "height and width have to be uneven"
m = Maze()
# m.generator = Prims((height-1)/2, (width-1)/2)
m.generator = Kruskal((height-1)/2, (width-1)/2)
m.generate()
m.start = (1, 1)
m.end = (height-2, width-2)
m.grid[m.start[1],m.start[0]] = 2
m.grid[m.end[1],m.end[0]] = 3

# make a tkinter window with a canvas that will show the maze
root = tk.Tk()
canvas = tk.Canvas(root, width=width*size_rectangle, height=height*size_rectangle)
canvas.pack()
fps = 2

# make a function to draw the maze
def draw_maze(grid, size):
    # clear the canvas
    canvas.delete("all")
    # loop over the grid
    for y in range(height):
        for x in range(width):
            # if the grid is a space
            if grid[y][x] == 0:
                # draw a black rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="white")
            # if the grid is a wall
            if grid[y][x] == 1:
                # draw a black rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="black")
            # if the grid is the start
            elif grid[y][x] == 2:
                # draw a green rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="green")
            # if the grid is the end
            elif grid[y][x] == 3:
                # draw a red rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="purple")
            # if the grid is a seen
            elif grid[y][x] == 4:
                # draw a blue rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="lightblue")
            # if the grid is a path
            elif grid[y][x] == 5:
                # draw a blue rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="red")
    # update the canvas
    canvas.update()

def bfs(grid, start):
    queue = collections.deque()
    queue.append(start)
    seen = set([start])
    # make two dim datastructur of size of the maze to store touples of x,y coordinates
    successor = [[0 for x in range(width)] for y in range(height)]
    path = []
    while queue:
        next_step = queue.popleft()
        # print(next_step)
        y, x = next_step
        if grid[y][x] == 3:
            # do backtracking to find the path
            while (y,x) != m.start:
                if grid[y,x] != 3:
                    grid[y,x] = 5
                path.append((y,x))
                y,x = successor[y][x]
            path.append(m.start)
            path.reverse()
            draw_maze(grid, size_rectangle)
            return True, path
        for y2, x2 in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)): #directions
            if ( 0 <= x2 < width and  #X-axis in range
                0 <= y2 < height and  #y-axis
                grid[y2][x2] != 1 and  #not a wall
                (y2, x2) not in seen): #not visited
                queue.append( (y2, x2))
                seen.add((y2, x2))
                successor[y2][x2] = (y,x)
                if grid[y2,x2] != 3:
                    grid[y2,x2] = 4
                draw_maze(grid, size_rectangle)
                #make a pause for 0.5 seconds
                # root.after(round(1000/fps))
    return False , path

success, path = bfs(m.grid, m.start)

print(success)
print(path)

root.mainloop()

