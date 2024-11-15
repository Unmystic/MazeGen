import random
from PIL import Image, ImageDraw
from grid import Cell, Grid
from recursive_backtracker import RecursiveBacktracker

class Cell3D(Cell):
    
    def __init__(self,level, row, column):
        self.level = level
        self.up, self.down = None, None
        super().__init__(row, column)
        
    def neighbours(self):
        nei =  super().neighbours()        
        if self.up:
            nei.append(self.up)
        if self.down:
            nei.append(self.down)
        
        return nei

class Grid3D(Grid):
    
    def __init__(self,levels, rows, columns):
        self.levels = levels
        super().__init__(rows, columns)
        
    def prepare_grid(self):
        grid = []
        for i in range(self.levels):
            level_list = []
            for j in range(self.rows):
                row_list = []
                for k in range(self.cols):
                    row_list.append(Cell3D(i,j,k))
                level_list.append(row_list)
            grid.append(level_list)
        return grid
    
    def configure_cells(self):
        for cell in self.each_cell():
            level, row, col =cell.level, cell.row, cell.col
            
            if row - 1 >= 0:
                cell.north = self.grid[level][row-1][col]
            if col - 1 >= 0:
                cell.west = self.grid[level][row][col-1]
            if row + 1 < self.rows:
                cell.south = self.grid[level][row+1][col]
            if col + 1 < self.cols:
                cell.east = self.grid[level][row][col+1]
            if level -1 >= 0:
                cell.down = self.grid[level-1][row][col]
            if level + 1 < self.levels:
                cell.up = self.grid[level+1][row][col]            
            
    def random_cell(self):
        level = random.randint(0, self.levels -1)
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)
        return self.grid[level][row][col]
    
    def size(self):
        return self.levels * self.rows * self.cols
    
    def each_level(self):
        for level in self.grid:
            yield level
    
    def each_row(self):
        for rows in self.each_level():
            for row in rows:
                yield row
    def each_cell(self):
        for level in self.grid:
            for row in level:
                for cell in row:
                    yield cell
    
    def to_png(self, cell_size=20, inset=0, margin = None, fname="../examples/3dmaze.png"):
        if margin is None:
            margin = cell_size // 2
        
        inset = int(cell_size * inset)
        grid_width = cell_size * self.cols
        grid_height = cell_size * self.rows
        
        img_width = grid_width * self.levels + (self.levels-1)* margin
        img_height = grid_height
        
        background = (255,255,255)
        wall = (0,0,0)
        arrow = (255,0,0)
        
        img = Image.new("RGB",(img_width+2,img_height+2),background)
        d = ImageDraw.Draw(img)
        
        for mode in ["background", "walls"]: # Draw background in first cycle, walls with second
            for cell in self.each_cell():
                x = cell.level * (grid_width+margin) + cell.col * cell_size
                y = cell.row * cell_size
                
                if inset > 0:
                    self.to_png_with_inset(img, d, cell, mode,cell_size, wall,x,y,inset)
                else:
                    self.to_png_without_inset(img, d, cell, mode,cell_size, wall,x,y)
                
                if mode == "walls":
                    mid_x = x + cell_size/2
                    mid_y = y + cell_size/2
                    
                    if cell.linked(cell.down):
                        d.line([mid_x-3,mid_y,mid_x-1,mid_y+2], fill=arrow)
                        d.line([mid_x-3,mid_y,mid_x-1,mid_y-2], fill=arrow)
                    if cell.linked(cell.up):
                        d.line([mid_x+3,mid_y,mid_x+1,mid_y+2], fill=arrow)
                        d.line([mid_x+3,mid_y,mid_x+1,mid_y-2], fill=arrow)                        
                
        img.save(fname,"PNG")


if __name__ == "__main__":
    
    grid = Grid3D(3,5,5)
    rback = RecursiveBacktracker()
    rback_grid = rback.on(grid)  
    fname = "../examples/3D_maze.png"
    rback_grid.to_png(cell_size=30,fname=fname)
    print(f"Created image {fname}")