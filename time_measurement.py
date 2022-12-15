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

side_length_square = 101
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
bfs_grid[m.end[1], m.end[0]] = 3

start_time = time.time()
success, path = bfs(bfs_grid, m.start, width, height)
end_time = time.time()
bfs_time = end_time-start_time
print("time bfs: ", bfs_time)

# for dfs
# build back the walls back up
dfs_grid = copy.deepcopy(m.grid)
dfs_grid[m.start[1], m.start[0]-1] = 1
dfs_grid[m.end[1], m.end[0]+1] = 1
# mark beginning and end
dfs_grid[m.start] = 2
dfs_grid[m.end[1], m.end[0]] = 3
# start timer
start = time.time()
success, path = dfs(dfs_grid, m.start, width, height)
#end timer
end = time.time()
dfs_time = end-start
print("time dfs: ", dfs_time)


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
ca_time = end_time-start_time
print("time CA: ", ca_time)


# plot
tensor_grid = tensor_grid.cpu().numpy()
grid_with_path = copy.deepcopy(m.grid)
grid_with_path[tensor_grid ==0] = 5

grids = [grid_with_path, bfs_grid, dfs_grid]
cmaps = [cmap2, cmap2, cmap2]
titles=[]
titles.append("CA " + "time: " + str(round(ca_time *1000,1)) + "ms")
titles.append("BFS " + "time: " + str(round(bfs_time *1000,1)) + "ms")
titles.append("DFS " + "time: " + str(round(dfs_time *1000,1)) + "ms")

showNPNG(grids, cmaps, titles)



