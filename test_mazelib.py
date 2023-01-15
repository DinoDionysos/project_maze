# tesing the mazelib library
# try the syntax to generate a maze
# print some meta information

from mazelib import Maze
from mazelib.generate.Kruskal import Kruskal
from util import showPNG

height = 7
width = 7
assert height % 2 == 1 and width % 2 == 1, "height and width have to be uneven"
# assert w >= 3 and h >= 3, "Mazes cannot be smaller than 3x3."
m = Maze()
# m.generator = Prims(height, width)
m.generator = Kruskal(int((height - 1) / 2), int((width - 1) / 2))
# m.solver = BacktrackingSolver()
# # make difficult maze (hard = long solution path), by taking 100 mazes, solve them 10 times with varying end and start points and take the one with the longest solution path
# m.generate_monte_carlo(100, 10, 1.0)
m.generate()
m.start = (1, 1)
# m.end = (2*height-1, 2*width-1)
m.end = (height - 2, width - 2)

m.grid[m.start[0], m.start[1]] = 2
m.grid[m.end[0], m.end[1]] = 3
print(m.grid)
print(type(m.grid))
print(m.start)
print(m.end)
print(type(m.start))
showPNG(m.grid)
