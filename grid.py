import random

class Cell(object):
    def __init__(self,row,column):
        self.row = row
        self.col = column
        self.north, self.south = None, None
        self.west, self.east = None, None
        self.links = {}
    
    # Connect two cells bidirectionaly
    def link(self, cell, bidir=True):
        self.links[cell] = True
        if bidir:
            cell.link(self,bidir=False)
    
    # Remove connection between two cells
    def unlink(self, cell, bidir=True):
        self.links.pop(cell)
        if bidir:
            cell.unlink(self,bidir=False)
    
    # Retieve all connection to current cell
    def links(self):
        return self.links.keys()
    
    # Check if two cells connected
    def linked(self,cell):
        return cell in self.links
    
    # Showing neighbour cells
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



class Grid(object):
    def __init__(self,rows,columns):
        self.rows = rows
        self.cols = columns
        self.grid = self.prepare_grid()
        self.configure_cells()
        
    def prepare_grid(self):
        grid = []
        for i in range(self.rows):
            row_list = []
            for j in range(self.cols):
                Cell(i,j)
                row_list.append(Cell(i,j))
            grid.append(row_list)
        return grid
    
    def configure_cells(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.grid[i][j]                             
                if i - 1 >= 0:
                    cell.north = self.grid[i-1][j]
                if j - 1 >= 0:
                    cell.west = self.grid[i][j-1]
                if i + 1 < self.rows:
                    cell.south = self.grid[i+1][j]
                if j + 1 < self.cols:
                    cell.east = self.grid[i][j+1]     
    
    def random_cell(self):
        
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)
        return self.grid[row][col]
    
    def size(self):
        return self.rows * self.cols
    
    def each_row(self):
        for row in self.grid:
            yield row
    
    def each_cell(self):
        for row in self.grid:
            for cell in row:
                yield cell
            
    
if __name__ == "__main__":
    
    grid = Grid(4,4)
    print(grid.grid)
    rand_cell = grid.random_cell()
    print([rand_cell.row, rand_cell.col], rand_cell.neighbours())
    print(grid.size())
    print(list(grid.each_row()))
    print(list(grid.each_cell()))
               
            
        