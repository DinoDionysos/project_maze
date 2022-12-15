from matplotlib import pyplot as plt

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