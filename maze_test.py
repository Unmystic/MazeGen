from PIL import Image, ImageDraw
from grid import Grid, Cell
import random
from recursive_backtracker import RecursiveBacktracker


if __name__ == "__main__":
    grid = Grid(15,15)
    rback = RecursiveBacktracker()
    rback_grid = rback.on(grid)
    
    deadends = rback_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    rback_grid.braid(0.5)
    
    deadends = rback_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    
    #print(rback_grid)
    
    rback_grid.to_png(cell_size=20, fname="test_maze.png",inset=0.1)
    print("Created image test_maze.png")