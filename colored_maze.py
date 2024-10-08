from grid import ColoredGrid
from sidewinder import Sidewinder

if __name__ == "__main__":
    
    grid = ColoredGrid(25,25)
    sidew = Sidewinder()
    s_grid = sidew.on(grid)
    
    start =s_grid.grid[s_grid.rows // 2][s_grid.cols // 2]
    
    s_grid.set_distances(start.distances())
    
    s_grid.to_png(cell_size= 15, fname="colored_maze")
    