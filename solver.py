import torch
import copy
import collections

def ca(grid, kernel):
    tensor_grid = torch.tensor(grid).float().cuda()
    # make convolution and padd the borders
    conv_grid = torch.nn.functional.conv2d(tensor_grid.unsqueeze(0).unsqueeze(0), kernel.unsqueeze(0).unsqueeze(0), padding=1).squeeze(0).squeeze(0)
    # where conv_grid >= 3, set tensor_grid to 1
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
        # where conv_grid >= 3, set tensor_grid to 1
        tensor_grid[conv_grid >= 3] = 1
        count += 1
    return count, tensor_grid

def bfs(grid, start, width, height):
    queue = collections.deque()
    queue.append(start)
    seen = set([start])
    # make two dim datastructur of size of the maze to store touples of x,y coordinates
    successor = [[0 for x in range(width)] for y in range(height)]
    path = []
    while queue:
        next_step = queue.popleft()
        # print(next_step)
        y, x = next_step
        if grid[y][x] == 3:
            # do backtracking to find the path
            while (y,x) != start:
                if grid[y,x] != 3:
                    grid[y,x] = 5
                path.append((y,x))
                y,x = successor[y][x]
            path.append(start)
            path.reverse()
            return True, path
        for y2, x2 in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)): #directions
            if ( 0 <= x2 < width and  #X-axis in range
                0 <= y2 < height and  #y-axis
                grid[y2][x2] != 1 and  #not a wall
                (y2, x2) not in seen): #not visited
                queue.append( (y2, x2))
                seen.add((y2, x2))
                successor[y2][x2] = (y,x)
                if grid[y2,x2] != 3:
                    grid[y2,x2] = 4
    return False , path

# function dfs
def dfs(grid, start, width, height):
    stack = collections.deque()
    stack.append(start)
    seen = set([start])
    # make two dim datastructur of size of the maze to store touples of x,y coordinates
    successor = [[0 for x in range(width)] for y in range(height)]
    path = []
    while stack:
        next_step = stack.pop()
        # print(next_step)
        y, x = next_step
        if grid[y][x] == 3:
            # do backtracking to find the path
            while (y,x) != start:
                if grid[y,x] != 3:
                    grid[y,x] = 5
                path.append((y,x))
                y,x = successor[y][x]
            path.append(start)
            path.reverse()
            return True, path
        for y2, x2 in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)): #directions
            if ( 0 <= x2 < width and  #X-axis in range
                0 <= y2 < height and  #y-axis
                grid[y2][x2] != 1 and  #not a wall
                (y2, x2) not in seen): #not visited
                stack.append( (y2, x2))
                seen.add((y2, x2))
                successor[y2][x2] = (y,x)
                if grid[y2,x2] != 3:
                    grid[y2,x2] = 4
    return False , path