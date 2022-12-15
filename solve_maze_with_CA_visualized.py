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

# make a tkinter window with a canvas that will show the maze
root = tk.Tk()
#make frame
frame = tk.Frame(root)
frame.pack()
# make two canvas in the frame next to each other
canvas = tk.Canvas(frame, width=width*size_rectangles, height=height*size_rectangles, bg="white")
canvas.pack(side=tk.LEFT)
canvas2 = tk.Canvas(frame, width=width*size_rectangles, height=height*size_rectangles, bg="white")
canvas2.pack(side=tk.LEFT)

# make a function to draw the maze with the size of the rectangles as a parameter
def draw_maze(grid, canvas, size):
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

# make function that takes an image as numpy array and then shows it on the canvas
def draw_image(grid, canvas, size):
    image = grid.cpu().numpy()
    # create new numpy array of size times the size of the image
    # use PIL to convert the numpy array to a PhotoImage
    # print shape of image
    print(image.shape)
    image = image / np.max(image) * 255
    image = Image.fromarray(image)
    image = image.resize((width*size, height*size))
    image = ImageTk.PhotoImage(image)
    # put it in the canvas
    canvas.create_image(0,0, image=image, anchor=tk.NW)
    # update the canvas
    canvas.update()

# make a function to draw the maze with the size of the rectangles as a parameter
def draw_maze2(grid, canvas, size):
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
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="red")
            # if the grid is a seen
            elif grid[y][x] == 4:
                # draw a blue rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="blue")
            # if the grid is a path
            elif grid[y][x] == 5:
                # draw a blue rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="blue")
            # if the grid is a path
            elif grid[y][x] == 6:
                # draw a blue rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="blue")
    # update the canvas
    canvas.update()

# print the type of the entries of m.grid
# transform m.grid to numpy array with type long
long_grid = m.grid.astype(np.long)

kernel = torch.tensor([[0,1,0],[1,0,1],[0,1,0]]).float().cuda()
# print kernel type
# save m.grid in a tensor with the same type as kernel
tensor_grid = torch.tensor(long_grid).float().cuda()
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
    draw_maze(tensor_grid, canvas, size_rectangles)
    # draw_maze2(conv_grid, canvas2, size_rectangles)
    #make a pause for 0.5 seconds
    root.after(round(1000/fps))

print("count: ", count)

# print(m.grid)
# conv_grid = conv_grid.cpu().numpy()
# show3PNG(m.grid, tensor_grid.cpu().numpy(), conv_grid>=3, plt.cm.binary, plt.cm.binary, plt.cm.binary)

# plot image with binary color with imshow
# plt.imshow(m.grid, cmap=cmap1, interpolation='nearest')

root.mainloop()



