from grid import Grid, Cell, ColoredGrid
import random
import os
from pathlib import Path

class RecursiveDivision(object):
    
    def on(self, grid):
        self.grid = grid
        
        for cell in grid.each_cell():
            for nei in cell.neighbours():
                cell.link(nei, False)
        
        self.divide(0,0,self.grid.rows, grid.cols)
        
        return grid
    
    def divide(self, row, column, height,width):
        
        # Basic algorithm case
        # if height <= 1 or width <= 1:
        #     return
        
        # Version with rooms
        if (height <= 1 or width <= 1 or
            (height<5 and width<5 and random.randint(0,3)==0)):
            return 
          
        if height > width:
            self.divide_horizontally(row,column,height,width)
        else:
            self.divide_vertically(row,column,height,width)
            
    def divide_horizontally(self, row, column,height,width):
        divide_south_of = random.randint(0, height-2)
        passage_at = random.randint(0,width -1)
        
        for x in range(width):
            if passage_at == x:
                pass
            else:
                cell = self.grid.grid[row+divide_south_of][column+x]
                if cell.south in cell.links:                    
                    cell.unlink(cell.south)
        self.divide(row,column,divide_south_of+1, width)
        self.divide(row+divide_south_of+1,column, height-divide_south_of-1, width)

    def divide_vertically(self, row, column,height,width):
        divide_east_of = random.randint(0, width-2)
        passage_at = random.randint(0,height -1)
        
        for y in range(height):
            if passage_at == y:
                pass
            else:
                cell = self.grid.grid[row+y][column+divide_east_of]
                if cell.east in cell.links:
                    cell.unlink(cell.east)
        self.divide(row,column,height, divide_east_of+1)
        self.divide(row,column+divide_east_of+1, height, width-divide_east_of-1)        
    
def colored_grid_image():
    grid = ColoredGrid(100,100)
    rdiv = RecursiveDivision()
    rdiv_grid = rdiv.on(grid)
        
    start =rdiv_grid.grid[rdiv_grid.rows // 2][rdiv_grid.cols // 2]       
    rdiv_grid.set_distances(start.distances())
    
    if not os.path.exists(os.path.abspath("examples/recursive_division")):
        os.makedirs("examples/recursive_division")
    
    fname = "examples/recursive_division/colored_recursive_division.png"
    rdiv_grid.to_png(cell_size=10,fname=fname)
    print(f"Created image {fname}")

if __name__ == "__main__":
    
    grid = Grid(20,20)
    rdiv = RecursiveDivision()
    rdiv_grid = rdiv.on(grid)  
    fname = "examples/recursive_division/recursive_division_with_rooms.png"
    rdiv_grid.to_png(cell_size=20,fname=fname)
    print(f"Created image {fname}")
    
    # colored_grid_image()