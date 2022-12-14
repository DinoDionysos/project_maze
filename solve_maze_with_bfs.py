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
np.random.seed(1)

height = 7
width = 7
assert height%2 == 1 and width%2==1, "height and width have to be uneven"
m = Maze()
# m.generator = Prims((height-1)/2, (width-1)/2)
m.generator = Kruskal((height-1)/2, (width-1)/2)
m.generate()
m.start = (1, 1)
m.end = (height-2, width-2)
m.grid[m.start[0],m.start[1]] = 2
m.grid[m.end[0],m.end[1]] = 3


cmap1 = ListedColormap(['white', 'black', (0.4,1,0.2), 'red'])
cmap2 = ListedColormap(['white', 'black', (0.4,1,0.2), 'red', (0,0.6,1)])

def showPNG(grid, cmap=None):
    """Generate a simple image of the maze."""
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=cmap, interpolation='nearest')
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
        x, y = next_step
        if grid[y][x] == 3:
            # do backtracking to find the path
            while (x,y) != m.start:
                path.append((x,y))
                x,y = successor[x][y]
            path.append(m.start)
            path.reverse()
            return True, path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)): #directions
            if ( 0 <= x2 < width and  #X-axis in range
                0 <= y2 < height and  #y-axis
                grid[x2][y2] != 1 and  #not a wall
                (x2, y2) not in seen): #not visited
                queue.append( (x2, y2))
                seen.add((x2, y2))
                successor[x2][y2] = (x,y)

    return False , path

print(m.grid)
showPNG(m.grid, cmap1)
success, path = bfs(m.grid, m.start)
for i,j in path:
    if (i,j) == m.start or (i,j) == m.end:
        continue
    m.grid[i,j] = 4

print(m.grid)
showPNG(m.grid, cmap2)

print(success)
