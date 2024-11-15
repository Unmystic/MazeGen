import math
from PIL import Image, ImageDraw
from grid import Grid, Cell
import random
from recursive_backtracker import RecursiveBacktracker
import heapq
from distances import Distances


class OverCell(Cell):
    def __init__(self, row, column, grid):
        super().__init__(row, column)
        self.grid = grid
    
    def neighbours(self):
        nei =  super().neighbours()
        
        if self.can_tunnel_north():
            nei.append(self.north.north)
        if self.can_tunnel_south():
            nei.append(self.south.south)
        if self.can_tunnel_west():
            nei.append(self.west.west)
        if self.can_tunnel_east():
            nei.append(self.east.east)
        return nei
    
    def can_tunnel_north(self):
        if self.north and self.north.north and self.north.horizontal_passage():
            return True
        else:
            return False
        
    def can_tunnel_south(self):
        if self.south and self.south.south and self.south.horizontal_passage():
            return True
        else:
            return False
    def can_tunnel_west(self):
        if self.west and self.west.west and self.west.vertical_passage():
            return True
        else:
            return False
    def can_tunnel_east(self):
        if self.east and self.east.east and self.east.vertical_passage():
            return True
        else:
            return False
        
    def horizontal_passage(self):
        return (self.linked(self.east) and self.linked(self.west) and 
                not self.linked(self.north) and not self.linked(self.south))
        
    def vertical_passage(self):
        return ( not self.linked(self.east) and not self.linked(self.west) and 
                self.linked(self.north) and self.linked(self.south))
        
    
    def link(self, cell, bidir=True):
        neighbor = None
        if self.north and self.north == cell.south:
            neighbor = self.north
        elif self.south and self.south == cell.north:
            neighbor = self.south
        elif self.west and self.west == cell.east:
            neighbor = self.west
        elif self.east and self.east == cell.west:
            neighbor = self.east
            
        if neighbor:
            self.grid.tunnel_under(neighbor)
        else:
            super().link(cell, bidir)
    
class UnderCell(Cell):
    def __init__(self, over_cell):
        super().__init__(over_cell.row, over_cell.col)
        
        if over_cell.horizontal_passage():
            self.north = over_cell.north
            over_cell.north.south = self
            self.south = over_cell.south
            over_cell.south.north = self
            self.link(self.north)
            self.link(self.south)
        else:
            self.east = over_cell.east
            over_cell.east.west = self
            self.west = over_cell.west
            over_cell.west.east = self
            self.link(self.east)
            self.link(self.west)
            
    def horizontal_passage(self):
        if self.east or self.west:
            return True
        else:
            return False
    
    def vertical_passage(self):
        if self.north or self.south:
            return True
        else:
            return False

class WeaveGrid(Grid):
    def __init__(self, rows, columns):
        self.under_cells = []
        super().__init__(rows, columns)
        
        
    def prepare_grid(self):
        grid = []
        for i in range(self.rows):
            row_list = []
            for j in range(self.cols):
                row_list.append(OverCell(i,j,self))
            grid.append(row_list)
        return grid
    
    def tunnel_under(self,over_cell):
        under_cell = UnderCell(over_cell)
        self.under_cells.append(under_cell)
    
    def each_cell(self):
        for row in self.grid:
            for cell in row:
                yield cell
        
        for cell in self.under_cells:
            yield cell
    
    def to_png(self, cell_size=20, inset=0.1, fname="../examples/weave_maze.png"):
        return super().to_png(cell_size = cell_size, inset = inset, fname=fname)
    
    def to_png_with_inset(self, img, d, cell, mode, cell_size, wall, x, y, inset):
        if cell.__class__.__name__ == "OverCell" or cell.__class__.__name__ == "SimpleOvercell":
            
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
                
    