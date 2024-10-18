from mask import Mask
from grid import MaskedGrid
from recursive_backtracker import RecursiveBacktracker
import sys

if __name__ == "__main__":
    l = len(sys.argv)
    if l == 1:
        print(" Input the name of the mask in CLI")
    else:
        mask =Mask.from_txt(sys.argv[1])
        grid = MaskedGrid(mask)
        rback = RecursiveBacktracker()
        rback.on(grid)
        
        grid.to_png(fname="stripped_maze.png")
        
        