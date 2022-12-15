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
import tkinter as tk
from PIL import Image, ImageTk
import time

# set seed for numpy shuffle
np.random.seed(2)

fps = 2
size_rectangles = 15

side_length_square = 31
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
m.grid[1,0] = 0
m.grid[height-2, width-1] = 0


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
    
def show3PNG(grid1, grid2, grid3, cmap1=None, cmap2=None, cmap3=None):
    """Generate a simple image of the maze."""
    fig = plt.figure(figsize=(10, 5))
    plt.subplot(1,3,1)
    plt.imshow(grid1, cmap=cmap1, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.subplot(1,3,2)
    plt.imshow(grid2, cmap=cmap2, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.subplot(1,3,3)
    plt.imshow(grid3, cmap=cmap3, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()

# print the type of the entries of m.grid
# transform m.grid to numpy array with type long
long_grid = m.grid.astype(np.long)

kernel = torch.tensor([[0,1,0],[1,0,1],[0,1,0]]).float().cuda()
# print kernel type
# save m.grid in a tensor with the same type as kernel
tensor_grid = torch.tensor(long_grid).float().cuda()
# start time
start_time = time.time()
# make convolution and padd the borders with ones
conv_grid = torch.nn.functional.conv2d(tensor_grid.unsqueeze(0).unsqueeze(0), kernel.unsqueeze(0).unsqueeze(0), padding=1).squeeze(0).squeeze(0)
# where conv_grid >= 7, set tensor_grid to 1
temp_grid = copy.deepcopy(tensor_grid)
tensor_grid[conv_grid >= 3] = 1
# while tensor_grid not equal to temp_grid
count = 0
# TODO problem: tensor_grid and temp_grid are the same but they shouldnt
while not torch.equal(tensor_grid, temp_grid):
    # temp = tensor_grid
    temp_grid = copy.deepcopy(tensor_grid)
    # make convolution
    conv_grid = torch.nn.functional.conv2d(tensor_grid.unsqueeze(0).unsqueeze(0), kernel.unsqueeze(0).unsqueeze(0), padding=1).squeeze(0).squeeze(0)
    # where conv_grid >= 7, set tensor_grid to 1
    tensor_grid[conv_grid >= 3] = 1
    count += 1
# end time
end_time = time.time()
print("time CA: ", end_time-start_time)
print("count: ", count)

conv_grid = conv_grid.cpu().numpy()
tensor_grid = tensor_grid.cpu().numpy()
grid_with_path = copy.deepcopy(m.grid)
grid_with_path[tensor_grid ==0] = 5
show3PNG(m.grid, tensor_grid, grid_with_path, plt.cm.binary, plt.cm.binary, cmap2)

# plot image with binary color with imshow
plt.imshow(m.grid, cmap=cmap1, interpolation='nearest')
