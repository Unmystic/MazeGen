import math
from PIL import Image, ImageDraw
from grid import Grid, Cell
import random
from recursive_backtracker import RecursiveBacktracker
from distances import Distances
from weave_grid import OverCell, WeaveGrid, UnderCell


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
            if left in self.set_for_cell and right in self.set_for_cell and self.set_for_cell[left] != self.set_for_cell[right]:
                return True
            else:
                return False
        
        def merge(self, left, right):
            # if left in self.set_for_cell and right in self.set_for_cell:
                left.link(right)
                winner = self.set_for_cell[left]         
                loser = self.set_for_cell[right]
                if loser in self.cells_in_set :
                    losers = self.cells_in_set[loser]
                else:
                    losers = [right]
                    
                for cell in losers:
                    self.cells_in_set[winner].append(cell)
                    self.set_for_cell[cell] = winner
                
                self.cells_in_set.pop(loser)
        
        def add_crossing(self, cell):
            if len(cell.links.keys()) > 0 or self.can_merge(cell.east, cell.west) == False or self.can_merge(cell.north, cell.south) == False:
                return False
            else:              
                self.neighbors = [[left,right] for [left,right] in self.neighbors if left != cell and right != cell]
                
                if random.randint(0,2) == 0:
                    self.merge(cell.west, cell)
                    self.merge(cell, cell.east)
                    
                    self.grid.tunnel_under(cell,self)
                    
                    self.merge(cell.north, cell.north.south)
                    self.merge(cell.south, cell.south.north)
                else:
                    self.merge(cell.north, cell)
                    self.merge(cell, cell.south)
                    
                    self.grid.tunnel_under(cell,self)
                    
                    self.merge(cell.west, cell.west.east)
                    self.merge(cell.east, cell.east.west)
            return True
                
    
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
    
class SimpleOvercell(OverCell):
    def neighbours(self):
        nei = []
        if self.north:
            nei.append(self.north)
        if self.south:
            nei.append(self.south)
        if self.west:
            nei.append(self.west)
        if self.east:
            nei.append(self.east)   
        return nei

class PreconfiguredGrid(WeaveGrid):
    def prepare_grid(self):
        grid = []
        for i in range(self.rows):
            row_list = []
            for j in range(self.cols):
                row_list.append(SimpleOvercell(i,j,self))
            grid.append(row_list)
        return grid
    
    def tunnel_under(self,over_cell,state):
        under_cell = UnderCell(over_cell)
        self.under_cells.append(under_cell)
        
        # Addition 
        s = len(state.set_for_cell)
        state.set_for_cell[under_cell] = s
        state.cells_in_set[s] = [under_cell]
        
        if under_cell.south:
            state.neighbors.append([under_cell, under_cell.south])
        if under_cell.east:
            state.neighbors.append([under_cell, under_cell.east])
    
    def to_png(self, cell_size=20, inset=0.1, fname="../examples/weave_maze.png"):
        return super().to_png(cell_size = cell_size, inset = inset, fname=fname)
    
    def to_png_with_inset(self, img, d, cell, mode, cell_size, wall, x, y, inset):
        if cell.__class__.__name__ == "SimpleOvercell":
            super().to_png_with_inset(img, d, cell, mode, cell_size, wall, x, y, inset)
        else:
            x1,x2,x3,x4,y1,y2,y3,y4 = self.cell_coordinates_with_inset(x,y,cell_size,inset)
            width = 1
            if cell.vertical_passage():
                d.line([x2,y1,x2,y2], fill=wall,width=width)
                d.line([x3,y1,x3,y2], fill=wall,width=width)
                d.line([x2,y3,x2,y4], fill=wall,width=width)
                d.line([x3,y3,x3,y4], fill=wall,width=width)
            else:
                d.line([x1,y2,x2,y2], fill=wall,width=width)
                d.line([x1,y3,x2,y3], fill=wall,width=width)
                d.line([x3,y2,x4,y2], fill=wall,width=width)
                d.line([x3,y3,x4,y3], fill=wall,width=width)

if __name__ == "__main__":
    
    grid = Grid(20,20)
    kru = Kruskals()
    kru_grid = kru.on(grid) 
    
    deadends = kru_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    kru_grid.braid(0.3)
    deadends = kru_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    
    fname = "../examples/kruskals_maze.png"
    kru_grid.to_png(cell_size=20,fname=fname)
    print(f"Created image {fname}")