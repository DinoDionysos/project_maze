import copy
import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
import torch
from matplotlib.colors import ListedColormap
from mazelib import Maze
from mazelib.generate.Kruskal import Kruskal

from util import draw_maze, getPytorchDevice

# set seed for numpy shuffle
np.random.seed(2)

fps = 2
size_rectangles = 15

side_length_square = 31
height = side_length_square
width = side_length_square
if height % 2 == 0:
    height += 1
    print("height has to be uneven, adding 1 to height")
if width % 2 == 0:
    width += 1
    print("width has to be uneven, adding 1 to width")

m = Maze()
# m.generator = Prims(int((height-1)/2), int((width-1)/2))
m.generator = Kruskal(int((height - 1) / 2), int((width - 1) / 2))
m.generate()
m.start = (1, 1)
m.end = (height - 2, width - 2)
m.grid[1, 0] = 0
m.grid[height - 2, width - 1] = 0

cmap1 = ListedColormap(['white', 'black', (0.4, 1, 0.2), 'blue'])
cmap2 = ListedColormap(['white', 'black', (0.4, 1, 0.2), 'blue', (0, 0.6, 1), 'red'])

# make a tkinter window with a canvas that will show the maze
root = tk.Tk()
# make frame
frame = tk.Frame(root)
frame.pack()
# make two canvas in the frame next to each other
canvas = tk.Canvas(frame, width=width * size_rectangles, height=height * size_rectangles, bg="white")
canvas.pack(side=tk.LEFT)
canvas2 = tk.Canvas(frame, width=width * size_rectangles, height=height * size_rectangles, bg="white")
canvas2.pack(side=tk.LEFT)

# print the type of the entries of m.grid
# transform m.grid to numpy array with type long
long_grid = m.grid.astype(np.long)

kernel = torch.tensor([[0, 1, 0], [1, 0, 1], [0, 1, 0]]).float().to(getPytorchDevice())
# print kernel type
# save m.grid in a tensor with the same type as kernel
tensor_grid = torch.tensor(long_grid).float().to(getPytorchDevice())
# make convolution and padd the borders with ones
conv_grid = torch.nn.functional.conv2d(tensor_grid.unsqueeze(0).unsqueeze(0), kernel.unsqueeze(0).unsqueeze(0),
                                       padding=1).squeeze(0).squeeze(0)
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
    conv_grid = torch.nn.functional.conv2d(tensor_grid.unsqueeze(0).unsqueeze(0), kernel.unsqueeze(0).unsqueeze(0),
                                           padding=1).squeeze(0).squeeze(0)
    # where conv_grid >= 7, set tensor_grid to 1
    tensor_grid[conv_grid >= 3] = 1
    count += 1
    draw_maze(tensor_grid, canvas, size_rectangles)
    # draw_maze2(conv_grid, canvas2, size_rectangles)
    # make a pause for 0.5 seconds
    root.after(round(1000 / fps))

print("count: ", count)

# print(m.grid)
# conv_grid = conv_grid.cpu().numpy()
# show3PNG(m.grid, tensor_grid.cpu().numpy(), conv_grid>=3, plt.cm.binary, plt.cm.binary, plt.cm.binary)

# plot image with binary color with imshow
# plt.imshow(m.grid, cmap=cmap1, interpolation='nearest')

root.mainloop()
