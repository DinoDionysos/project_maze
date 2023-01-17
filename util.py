import torch
from matplotlib import pyplot as plt


def getPytorchDevice():
    if torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cuda")


def showPNG(grid, cmap=None):
    """Generate a simple image of the maze."""
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=cmap, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()


def show2PNG(grid1, grid2, cmap1=None, cmap2=None):
    """Generate a simple image of the maze."""
    fig = plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(grid1, cmap=cmap1, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.subplot(1, 2, 2)
    plt.imshow(grid2, cmap=cmap2, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()


def show3PNG(grid1, grid2, grid3, cmap1=None, cmap2=None, cmap3=None):
    """Generate a simple image of the maze."""
    fig = plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(grid1, cmap=cmap1, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.subplot(1, 3, 2)
    plt.imshow(grid2, cmap=cmap2, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.subplot(1, 3, 3)
    plt.imshow(grid3, cmap=cmap3, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()


def showNPNG(grids, cmaps, titles):
    """Generate a simple image of the maze."""
    fig = plt.figure(figsize=(10, 5))
    for i in range(len(grids)):
        plt.subplot(1, len(grids), i + 1)
        plt.imshow(grids[i], cmap=cmaps[i], interpolation='nearest')
        plt.xticks([]), plt.yticks([])
        plt.title(titles[i])
    plt.show()


def draw_maze(grid, canvas, size):
    """ make a function to draw the maze with the size of the rectangles as a parameter"""
    height = len(grid)
    width = len(grid[0])
    # clear the canvas
    canvas.delete("all")
    # loop over the grid
    for y in range(height):
        for x in range(width):
            # if the grid is a space
            if grid[y][x] == 0:
                # draw a black rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="white")
            # if the grid is a wall
            if grid[y][x] == 1:
                # draw a black rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="black")
            # if the grid is the start
            elif grid[y][x] == 2:
                # draw a green rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="green")
            # if the grid is the end
            elif grid[y][x] == 3:
                # draw a red rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="purple")
            # if the grid is a seen
            elif grid[y][x] == 4:
                # draw a blue rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="#08f")
            # if the grid is a path
            elif grid[y][x] == 5:
                # draw a red rectangle
                canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill="red")
    # update the canvas
    canvas.update()


def draw_maze2(grid, canvas, size):
    """make a function to draw the maze with the size of the rectangles as a parameter"""
    height = len(grid)
    width = len(grid[0])
    # clear the canvas
    canvas.delete("all")
    # loop over the grid
    for y in range(height):
        for x in range(width):
            # if the grid is a space
            if grid[y][x] == 0:
                # draw a black rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="white")
            # if the grid is a wall
            if grid[y][x] == 1:
                # draw a black rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="black")
            # if the grid is the start
            elif grid[y][x] == 2:
                # draw a green rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="green")
            # if the grid is the end
            elif grid[y][x] == 3:
                # draw a red rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="red")
            # if the grid is a seen
            elif grid[y][x] == 4:
                # draw a blue rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="blue")
            # if the grid is a path
            elif grid[y][x] == 5:
                # draw a blue rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="blue")
            # if the grid is a path
            elif grid[y][x] == 6:
                # draw a blue rectangle
                canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill="blue")
    # update the canvas
    canvas.update()
