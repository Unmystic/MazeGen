from grid import Grid
from recursive_backtracker import RecursiveBacktracker

grid = Grid(5,5)

grid.grid[0][0].east.west = None
grid.grid[0][0].south.north = None

grid.grid[4][4].west.east = None
grid.grid[4][4].north.south = None
rback = RecursiveBacktracker()

rback.on(grid=grid,start_at=grid.grid[1][1])

print(grid)