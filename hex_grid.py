import math
from PIL import Image, ImageDraw
from grid import Grid, Cell
import random
from recursive_backtracker import RecursiveBacktracker

class HexCell(Cell):

    def __init__(self, row, column):
        super().__init__(row, column)
        self.northeast, self.northwest = None, None
        self.southeast, self.southwest = None, None
        
    
    def neighbours(self):
        nei = []
        if self.north:
            nei.append(self.north)
        if self.northeast:
            nei.append(self.northeast)
        if self.northwest:
            nei.append(self.northwest)
        if self.south:
            nei.append(self.south)
        if self.southeast:
            nei.append(self.southeast)
        if self.southwest:
            nei.append(self.southwest)
        return nei
    
class HexGrid(Grid):
    
    def __init__(self, rows,cols):
        super().__init__(rows, cols)
    
    def prepare_grid(self):
        grid = []
        for i in range(self.rows):
            row_list = []
            for j in range(self.cols):
                row_list.append(HexCell(i,j))
            grid.append(row_list)
        return grid
    
    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.col
            if col % 2 == 0:
                north_diagonal = row -1
                south_diagonal = row 
            else:
                north_diagonal = row
                south_diagonal = row + 1
            
            if row - 1 >= 0:
                cell.north = self.grid[row-1][col]
            if col - 1 >= 0 :
                cell.northwest = self.grid[north_diagonal][col-1]
                cell.southwest = self.grid[south_diagonal][col-1]
            if row + 1 < self.rows:
                cell.south = self.grid[row+1][col]
            if col + 1 < self.cols:
                cell.northeast = self.grid[north_diagonal][col+1]
                cell.southeast= self.grid[south_diagonal][col+1] 
    
    def to_png(self, cell_size=10, fname="hex_maze.png"):
        
        pass 