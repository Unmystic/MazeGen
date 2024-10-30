from PIL import Image, ImageDraw
from grid import Grid, Cell
from weave_grid import WeaveGrid
import random
from recursive_backtracker import RecursiveBacktracker


if __name__ == "__main__":
    grid = WeaveGrid(20,20)
    rback = RecursiveBacktracker()
    rback_grid = rback.on(grid)
    
    # deadends = rback_grid.deadends()
    # print(f"The maze has {len(deadends)} deadends")
    # rback_grid.braid(0.5)
    
    # deadends = rback_grid.deadends()
    # print(f"The maze has {len(deadends)} deadends")
    
    #print(rback_grid)
    fname = "weave_maze.png"
    rback_grid.to_png(cell_size=20,fname=fname, inset=0.1)
    print(f"Created image {fname}")