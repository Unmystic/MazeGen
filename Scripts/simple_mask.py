from mask import Mask
from grid import MaskedGrid
from recursive_backtracker import RecursiveBacktracker

if __name__ == "__main__":
    
    mask = Mask(5,5)
    mask.set_switch(0,0, False)
    mask.set_switch(2,2, False)
    mask.set_switch(4,4, False)
    
    grid = MaskedGrid(mask)
    rback = RecursiveBacktracker()
    rback.on(grid)
    
    grid.to_png(fname="../examples/simple_mask.png")
    
    print(grid)