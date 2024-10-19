from mask import Mask
from grid import MaskedGrid
from recursive_backtracker import RecursiveBacktracker
import sys

if __name__ == "__main__":
    l = len(sys.argv)
    if l == 1:
        print(" Input the name of the mask in CLI")
    else:
        mask =Mask.from_png(sys.argv[1])
        grid = MaskedGrid(mask)
        rback = RecursiveBacktracker()
        rback.on(grid)
        
        grid.to_png(cell_size=15,fname=f"maze_{sys.argv[1]}")
        print(f"Image saved as maze_{sys.argv[1]}")
        
        