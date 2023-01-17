from mazelib.generate.Prims import Prims
from mazelib.generate.Kruskal import Kruskal
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import torch
from matplotlib.colors import ListedColormap
import numpy as np
import copy
import time

from util import *
from solver import *



# set seed for numpy shuffle
np.random.seed(2)

size_rectangles = 30
cmap1 = ListedColormap(['white', 'black', (0.4,1,0.2), 'purple'])
cmap2 = ListedColormap(['white', 'black', (0.4,1,0.2), 'purple', (0,0.4,0.8), 'red'])

side_length_square = 201
height = side_length_square
width = side_length_square

absolute_time_bfs = 0
absolute_time_dfs = 0
absolute_time_ca = 0
absolute_count_steps_ca = 0
absolute_count_steps_bfs = 0
absolute_count_steps_dfs = 0

number_of_time_measurements = 1000
print_every_iteration = 50

m = Maze()

if height%2 == 0:
    height += 1
    print("height has to be uneven, adding 1 to height")
if width%2==0:
    width += 1
    print("width has to be uneven, adding 1 to width")

# do CA one time to let it allocate its memory
####################################################
# m.generator = Prims((height-1)/2, (width-1)/2)
m.generator = Kruskal((height-1)/2, (width-1)/2)
m.generate()
# print(m.grid)
m.start = (1, 1)
m.end = (height-2, width-2)
ca_grid = copy.deepcopy(m.grid)
ca_grid[m.start[0], m.start[1]-1] = 0
ca_grid[m.end[0], m.end[1]+1] = 0
kernel = torch.tensor([[0,1,0],[1,0,1],[0,1,0]]).float().cuda()
ca_grid = torch.tensor(ca_grid).float().to(getPytorchDevice())
count_steps_ca, tensor_grid = ca(ca_grid, kernel)
####################################################

for iteration_number in range(number_of_time_measurements):
    iteration_number += 1
    m.generator = Prims((height-1)/2, (width-1)/2)
    #m.generator = Kruskal((height-1)/2, (width-1)/2)
    m.generate()
    # print(m.grid)
    m.start = (1, 1)
    m.end = (height-2, width-2)

    # get the number of zeros in m.grid
    num_ones = np.count_nonzero(m.grid == 0)

    # for bfs
    bfs_grid = copy.deepcopy(m.grid)
    bfs_grid[m.start[0], m.start[1]-1] = 1
    bfs_grid[m.end[0], m.end[1]+1] = 1
    # mark beginning and end
    bfs_grid[m.start] = 2
    bfs_grid[m.end[0], m.end[1]] = 3
    # start timer bfs
    start_time = time.time()
    success, path, bfs_seen = bfs(bfs_grid, m.start)
    end_time = time.time()
    bfs_time = end_time-start_time
    # add absolute time and steps
    count_steps_bfs = len(bfs_seen)
    bfs_frac_seen = count_steps_bfs/num_ones
    absolute_count_steps_bfs += count_steps_bfs
    absolute_time_bfs += bfs_time
    # print("time bfs: ", str(round(bfs_time *1000,4)), "frac seen: ", str(round(bfs_frac_seen,2)))

    # for dfs
    dfs_grid = copy.deepcopy(m.grid)
    dfs_grid[m.start[0], m.start[1]-1] = 1
    dfs_grid[m.end[0], m.end[1]+1] = 1
    # mark beginning and end
    dfs_grid[m.start] = 2
    dfs_grid[m.end[0], m.end[1]] = 3
    # start timer
    start = time.time()
    success, path, dfs_seen = dfs(dfs_grid, m.start)
    #end timer
    end = time.time()
    dfs_time = end-start
    # add absolute time and steps
    count_steps_dfs = len(dfs_seen)
    dfs_frac_seen = count_steps_dfs/num_ones
    absolute_count_steps_dfs += count_steps_dfs
    absolute_time_dfs += dfs_time
    # print("time dfs: ", str(round(dfs_time *1000,4)), "frac seen: ", str(round(dfs_frac_seen,2)))


    # for CA
    ca_grid = copy.deepcopy(m.grid)
    ca_grid[m.start[0], m.start[1]-1] = 0
    ca_grid[m.end[0], m.end[1]+1] = 0
    kernel = torch.tensor([[0,1,0],[1,0,1],[0,1,0]]).float().cuda()
    # start time
    start_time = time.time()
    count_steps_ca, tensor_grid = ca(ca_grid, kernel)
    # end time
    end_time = time.time()
    ca_time = end_time-start_time
    # add absolute time
    absolute_time_ca += ca_time
    absolute_count_steps_ca += count_steps_ca
    # print("time CA: ", str(round(ca_time *1000,4)))
    # print("count steps CA: ", count)

    if (iteration_number%print_every_iteration == 0):
        print("######################## iteration_number = ", iteration_number)
        mean_time_bfs = absolute_time_bfs / iteration_number
        mean_time_dfs = absolute_time_dfs / iteration_number
        mean_time_ca = absolute_time_ca / iteration_number
        mean_count_steps_ca = absolute_count_steps_ca / iteration_number
        mean_count_steps_bfs = absolute_count_steps_bfs / iteration_number
        mean_count_steps_dfs = absolute_count_steps_dfs / iteration_number
        print("BFS abs time: " + str(round(absolute_time_bfs *1000,1)) + "ms")
        print("DFS abs time: " + str(round(absolute_time_dfs *1000,1)) + "ms")
        print("CA abs time: " + str(round(absolute_time_ca *1000,1)) + "ms")
        print("BFS mean time: " + str(round(mean_time_bfs *1000,1)) + "ms")
        print("DFS mean time: " + str(round(mean_time_dfs *1000,1)) + "ms")
        print("CA mean time: " + str(round(mean_time_ca *1000,1)) + "ms")
        print("BFS current time: " + str(round(bfs_time *1000,1)) + "ms")
        print("DFS current time: " + str(round(dfs_time *1000,1)) + "ms")
        print("CA current time: " + str(round(ca_time *1000,1)) + "ms")
        print("BFS absolute number of steps needed: " + str(absolute_count_steps_bfs))
        print("DFS absolute number of steps needed: " + str(absolute_count_steps_dfs))
        print("CA absolute number of steps needed: " + str(absolute_count_steps_ca))
        print("BFS mean number of steps needed: " + str(mean_count_steps_bfs))
        print("DFS mean number of steps needed: " + str(mean_count_steps_dfs))
        print("CA mean number of steps needed: " + str(mean_count_steps_ca))
        print("BFS current number of steps needed: " + str(count_steps_bfs))
        print("DFS current number of steps needed: " + str(count_steps_dfs))
        print("CA current number of steps needed: " + str(count_steps_ca))

# mean_time_bfs = absolute_time_bfs / number_of_time_measurements
# mean_time_dfs = absolute_time_dfs / number_of_time_measurements
# mean_time_ca = absolute_time_ca / number_of_time_measurements
# print("BFS mean time: " + str(round(mean_time_bfs *1000,1)) + "ms")
# print("DFS mean time: " + str(round(mean_time_dfs *1000,1)) + "ms")
# print("CA mean time: " + str(round(mean_time_ca *1000,1)) + "ms")