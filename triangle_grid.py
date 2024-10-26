import math
from PIL import Image, ImageDraw
from grid import Grid, Cell
import random
from recursive_backtracker import RecursiveBacktracker

class TriangleCell(Cell):
    
    def upright(self):
        return (self.row + self.col) % 2  == 0
    
    def neighbours(self):
        nei = []
        upright = self.upright()
        if self.north and not upright:
            nei.append(self.north)
        if self.south and upright:
            nei.append(self.south)
        if self.west:
            nei.append(self.west)
        if self.east:
            nei.append(self.east)   
        return nei
    
    
class TriangleGrid(Grid):
    
    def prepare_grid(self):
        grid = []
        for i in range(self.rows):
            row_list = []
            for j in range(self.cols):
                row_list.append(TriangleCell(i,j))
            grid.append(row_list)
        return grid
    
    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.col
            
            if col - 1 >= 0:
                cell.west = self.grid[row][col-1]
            
            if col + 1 < self.cols:
                cell.east = self.grid[row][col+1]   
                     
            if cell.upright() and row + 1 < self.rows:
                cell.south = self.grid[row+1][col]            
            if not cell.upright() and  row - 1 >= 0 :
                cell.north = self.grid[row-1][col]

    def background_colour_cell(self, cell):
        return (255,255,255,255)
                   
    def to_png(self, size=20, fname="tri_maze.png"):
        half_width = size / 2
        height = (size * math.sqrt(3)) / 2
        half_height = height / 2
        
        img_width = int(size * (self.cols + 1) / 2)
        img_height = int(height * self.rows)
        
        img = Image.new("RGBA",(img_width+2,img_height+2),(255,255,255,0))
        d = ImageDraw.Draw(img)
        wall = (0,0,0,255)
        for mode in ["background", "walls"]: # Draw background in first cycle, walls with second
            for cell in self.each_cell():
                # center point of cell
                cx = half_width + cell.col * half_width
                cy = half_height + cell.row * height
                
                west_x = cx - half_width
                mid_x = cx
                east_x = cx + half_width
                
                upright = cell.upright()
                if upright:
                    apex_y = cy - half_height
                    base_y = cy + half_height
                else:
                    apex_y = cy + half_height
                    base_y = cy - half_height
                

                if mode == "background":
                    colour = self.background_colour_cell(cell)
                    if colour:
                        points = [(west_x, base_y), (mid_x, apex_y), (east_x, base_y)]
                        d.polygon(xy=points,fill=colour)
                        
                else:
                    if not cell.west:
                        d.line([west_x, base_y, mid_x, apex_y], fill=wall,width=2)
                    if not cell.linked(cell.east):
                        d.line([east_x, base_y, mid_x, apex_y], fill=wall,width=2)
                        
                    no_south = cell.upright() and cell.south is None
                    not_linked = not cell.upright() and not cell.linked(cell.north)
                    
                    if no_south or not_linked:
                        d.line([east_x, base_y, west_x,base_y], fill = wall, width=2)
                        
        img.save(fname,"PNG")  
        
if __name__ == "__main__":
    
    grid = TriangleGrid(10,17)
    rback = RecursiveBacktracker()
    rback.on(grid)
    
    grid.to_png(size=30,fname="delta_maze.png")
    print("Image created delta_maze.png")