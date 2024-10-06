from grid import Grid, DistanceGrid, Cell
from sidewinder import Sidewinder

if __name__ == "__main__":
    grid = DistanceGrid(16,16)
    sidew = Sidewinder()
    s_grid = sidew.on(grid)
    # print(s_grid)
    start = s_grid.grid[0][0]
    distances = start.distances()
    s_grid.distances = distances
    print(s_grid)