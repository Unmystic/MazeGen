from grid import Grid, DistanceGrid, Cell
from sidewinder import Sidewinder

if __name__ == "__main__":
    grid = DistanceGrid(8,8)
    sidew = Sidewinder()
    s_grid = sidew.on(grid)
    #print(s_grid)
    start = s_grid.grid[0][0]
    
    # First algo loop
    distances = start.distances()
    new_start, distance = distances.max_path()
    
    # second algo loop
    new_distances =  new_start.distances()
    goal, distance = new_distances.max_path()
    
    s_grid.distances = new_distances.path_to_goal(goal)
    print(s_grid)