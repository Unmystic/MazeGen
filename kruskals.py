import math
from PIL import Image, ImageDraw
from grid import Grid, Cell
import random
from recursive_backtracker import RecursiveBacktracker
from distances import Distances


class Kruskals(object):
    
    class State(object):
        def __init__(self, grid):
            self.grid = grid 
            self.neighbors = []
            self.set_for_cell = {}
            self.cells_in_set = {}
            
            for cell in grid.each_cell():
                s = len(self.set_for_cell)
                self.set_for_cell[cell] = s
                self.cells_in_set[s] = [cell]
                
                if cell.south:
                    self.neighbors.append([cell, cell.south])
                if cell.east:
                    self.neighbors.append([cell, cell.east])
        
        def can_merge(self, left,right):
            return self.set_for_cell[left] != self.set_for_cell[right]
        
        def merge(self, left, right):
            left.link(right)
            
            winner = self.set_for_cell[left]
            loser = self.set_for_cell[right]
            if loser in self.cells_in_set and self.cells_in_set[loser]:
                losers = self.cells_in_set[loser]
            else:
                losers = [right]
                
            for cell in losers:
                self.cells_in_set[winner].append(cell)
                self.set_for_cell[cell] = winner
            
            self.cells_in_set.pop(loser)
    
    def on(self, grid, state =None):
        if state is None:
            state = self.State(grid=grid)
        
        neighbors = state.neighbors
        random.shuffle(neighbors)
        
        while neighbors:
            left,right = neighbors.pop()
            if state.can_merge(left,right):
                state.merge(left,right)
        
        return grid

if __name__ == "__main__":
    
    grid = Grid(20,20)
    kru = Kruskals()
    kru_grid = kru.on(grid) 
    
    deadends = kru_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    kru_grid.braid(0.3)
    deadends = kru_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    
    fname = "kruskals_maze.png"
    kru_grid.to_png(cell_size=20,fname=fname)
    print(f"Created image {fname}")