from mazelib.generate.Prims import Prims
from mazelib.generate.Kruskal import Kruskal
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import torch
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import collections
import numpy as np
import copy
import time

from util import *
from solver import *



# set seed for numpy shuffle
np.random.seed(2)

size_rectangles = 15
cmap1 = ListedColormap(['white', 'black', (0.4,1,0.2), 'blue'])
cmap2 = ListedColormap(['white', 'black', (0.4,1,0.2), 'blue', (0,0.6,1), 'red'])

side_length_square = 201
height = side_length_square
width = side_length_square

m = Maze()

if height%2 == 0:
    height += 1
    print("height has to be uneven, adding 1 to height")
if width%2==0:
    width += 1
    print("width has to be uneven, adding 1 to width")


# m.generator = Prims((height-1)/2, (width-1)/2)
m.generator = Kruskal((height-1)/2, (width-1)/2)
m.generate()
m.start = (1, 1)
m.end = (height-2, width-2)

# for bfs
# build back the walls back up
bfs_grid = copy.deepcopy(m.grid)
bfs_grid[m.start[1], m.start[0]-1] = 1
bfs_grid[m.end[1], m.end[0]+1] = 1
# mark beginning and end
bfs_grid[m.start] = 2
bfs_grid[m.end[1]-2, m.end[0]-2] = 3

start_time = time.time()
success, path = bfs(bfs_grid, m.start, width, height)
end_time = time.time()
print("time bfs: ", end_time-start_time)

# for dfs
# build back the walls back up
dfs_grid = copy.deepcopy(m.grid)
dfs_grid[m.start[1], m.start[0]-1] = 1
dfs_grid[m.end[1], m.end[0]+1] = 1
# mark beginning and end
dfs_grid[m.start] = 2
dfs_grid[m.end[1]-2, m.end[0]-2] = 3
# start timer
start = time.time()
success, path = dfs(dfs_grid, m.start, width, height)
#end timer
end = time.time()
print("time dfs: ", end - start)


# for CA
ca_grid = copy.deepcopy(m.grid)
ca_grid[m.start[1], m.start[0]-1] = 0
ca_grid[m.end[1], m.end[0]+1] = 0
kernel = torch.tensor([[0,1,0],[1,0,1],[0,1,0]]).float().cuda()

# start time
start_time = time.time()
count, tensor_grid = ca(ca_grid, kernel)
# end time
end_time = time.time()
print("count: ", count)
print("time CA: ", end_time-start_time)





