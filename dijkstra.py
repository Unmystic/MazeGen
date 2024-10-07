from grid import Grid, DistanceGrid, Cell
from sidewinder import Sidewinder

if __name__ == "__main__":
    grid = DistanceGrid(8,8)
    sidew = Sidewinder()
    s_grid = sidew.on(grid)
    print(s_grid)
    start = s_grid.grid[0][0]
    distances = start.distances()
    s_grid.distances = distances.cells
    print(s_grid)
    print("Path from northwest corner to southwest corner: ")
    s_grid.distances = distances.path_to_goal(s_grid.grid[s_grid.rows -1][0])
    print(s_grid)