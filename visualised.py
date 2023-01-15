import copy
import tkinter as tk
from copy import deepcopy

import numpy as np
from mazelib import Maze
from mazelib.generate.Kruskal import Kruskal

from solver import dfs, bfs, ca

# set seed for numpy shuffle
np.random.seed(2)
size_rectangles = 15
side_length_square = 31
height = side_length_square
width = side_length_square
assert height % 2 == 1 and width % 2 == 1, "height and width have to be uneven"

# maze init
m = Maze()
m.generator = Kruskal(int((height - 1) / 2), int((width - 1) / 2))
m.generate()
m.start = (1, 1)
m.end = (height - 2, width - 2)
m.grid[m.start[1], m.start[0]] = 2
m.grid[m.end[1], m.end[0]] = 3

algorithms = [ca, dfs, bfs]
algo_canvas = []
algo_grids = []
# make a tkinter window with a canvas that will show the maze
root = tk.Tk()

# copy grid for each algo
for idx, algo in enumerate(algorithms):
    algo_grids.append(copy.deepcopy(m))

# create window and canvas for each algo
for algo in algorithms:
    window = tk.Toplevel(root)
    canvas = tk.Canvas(window, width=width * size_rectangles, height=height * size_rectangles)
    canvas.pack()
    algo_canvas.append(canvas)

for idx, algo in enumerate(algorithms):
    maze = algo_grids[idx]
    grid = maze.grid
    print(algo.__name__)
    if algo.__name__ == 'ca':
        grid = np.array(grid)
    print(grid)
    success, path, seen = algo(grid, maze.start, algo_canvas[idx], size_rectangles)

root.mainloop()
