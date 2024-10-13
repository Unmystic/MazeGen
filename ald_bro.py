# Implementation of Aldous-Broder algorithm, creating random walks
import random
from grid import Grid, ColoredGrid


class AldousBroder(object):
    
    def on(self, grid):
        cell = grid.random_cell()
        unvisited = grid.size() - 1
        
        while unvisited > 0 :
            neighbor = random.choice(cell.neighbours())
            if not neighbor.links :
                cell.link(neighbor)
                unvisited -= 1
            cell = neighbor
        
        return grid
    
if __name__ == "__main__":
    
    grid = Grid(25,25)
    ab = AldousBroder()
    ab_grid = ab.on(grid)
    
    ab_grid.to_png(cell_size=20, fname="aldous_broder")