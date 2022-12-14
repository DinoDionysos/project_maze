from mazelib.generate.Prims import Prims
from mazelib.generate.Kruskal import Kruskal
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import torch
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import collections

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

def showPNG(grid):
    """Generate a simple image of the maze."""
    fig = plt.figure(figsize=(10, 5))
    cmap = ListedColormap(['white', 'black', (0.4,1,0.2), 'red'])#, (0,0.6,1)])
    plt.imshow(grid, cmap=cmap, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()

def bfs(grid, start):
    queue = collections.deque()
    queue.append(start)
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path
        if grid[y][x] == goal:
            return True
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)): #directions
            if ( 0 <= x2 < width and  #X-axis in range
                0 <= y2 < height and  #y-axis
                grid[y2][x2] != wall and  #not a wall
                (x2, y2) not in seen): #not visited
                queue.append( (x2, y2))
                seen.add((x2, y2))
    return False


showPNG(m.grid)
