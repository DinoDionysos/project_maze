from mazelib.generate.Prims import Prims
from mazelib.generate.Kruskal import Kruskal
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import torch
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import collections
import numpy as np

# set seed for numpy shuffle
# np.random.seed(2)

side_length_square = 101
height = side_length_square
width = side_length_square
if height%2 == 0:
    height += 1
    print("height has to be uneven, adding 1 to height")
if width%2==0:
    width += 1
    print("width has to be uneven, adding 1 to width")

m = Maze()
# m.generator = Prims((height-1)/2, (width-1)/2)
m.generator = Kruskal((height-1)/2, (width-1)/2)
m.generate()
m.start = (1, 1)
m.end = (height-2, width-2)
m.grid[m.start[1],m.start[0]] = 2
m.grid[m.end[1],m.end[0]] = 3


cmap1 = ListedColormap(['white', 'black', (0.4,1,0.2), 'blue'])
cmap2 = ListedColormap(['white', 'black', (0.4,1,0.2), 'blue', (0,0.6,1), 'red'])

def showPNG(grid, cmap=None):
    """Generate a simple image of the maze."""
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=cmap, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()

def show2PNG(grid1, grid2, cmap1=None, cmap2=None):
    """Generate a simple image of the maze."""
    fig = plt.figure(figsize=(10, 5))
    plt.subplot(1,2,1)
    plt.imshow(grid1, cmap=cmap1, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.subplot(1,2,2)
    plt.imshow(grid2, cmap=cmap2, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()

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
    return False , path


import copy
save_grid = copy.deepcopy(m.grid)
save_grid[0,0] = 0
# solve mazeand do backtracking
import time
start_time = time.time()
success, path = bfs(m.grid, m.start)
end_time = time.time()
print("time bfs: ", end_time-start_time)


m.grid[0,0] = 0
show2PNG(save_grid, m.grid, cmap1, cmap2)

print(success)
