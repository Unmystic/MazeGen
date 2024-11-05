from PIL import Image, ImageDraw
from grid import Grid, Cell
from weave_grid import WeaveGrid
import random
from recursive_backtracker import RecursiveBacktracker
from kruskals import PreconfiguredGrid, Kruskals


if __name__ == "__main__":
    
    grid = PreconfiguredGrid(20,20)
    state = Kruskals.State(grid)
    
    for i in range(grid.size()):
        row = 1 + random.randint(0, grid.rows - 3)
        col = 1 + random.randint(0, grid.cols - 3)
        state.add_crossing(grid.grid[row][col])
    
    kru = Kruskals()
    kru_grid = kru.on(grid) 
    
    # deadends = rback_grid.deadends()
    # print(f"The maze has {len(deadends)} deadends")
    # rback_grid.braid(0.5)
    
    # deadends = rback_grid.deadends()
    # print(f"The maze has {len(deadends)} deadends")
    
    #print(rback_grid)
    fname = "weaved_kruskals.png"
    kru_grid.to_png(cell_size=20,fname=fname, inset=0.2)
    print(f"Created image {fname}")