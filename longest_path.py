from grid import Grid, DistanceGrid, Cell
from sidewinder import Sidewinder
from recursive_backtracker import RecursiveBacktracker

if __name__ == "__main__":
    grid = DistanceGrid(10,10)
    
    # sidew = Sidewinder()
    # s_grid = sidew.on(grid)
    rback = RecursiveBacktracker()
    rback_grid = rback.on(grid)
    
    rback_grid.braid(0.5)
    #print(s_grid)
    start = rback_grid.grid[0][0]
    
    # First algo loop
    distances = start.distances()
    new_start, distance = distances.max_path()
    
    # second algo loop
    new_distances =  new_start.distances()
    goal, distance = new_distances.max_path()
    
    rback_grid.distances = new_distances.path_to_goal(goal)
    print(rback_grid)