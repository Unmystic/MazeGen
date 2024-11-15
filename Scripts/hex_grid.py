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
            if col - 1 >= 0  and north_diagonal >=0:
                cell.northwest = self.grid[north_diagonal][col-1]
            if col - 1 >= 0  and south_diagonal < self.rows:
                cell.southwest = self.grid[south_diagonal][col-1]
            if row + 1 < self.rows:
                cell.south = self.grid[row+1][col]
            if col + 1 < self.cols and north_diagonal >=0:
                cell.northeast = self.grid[north_diagonal][col+1]
            if col + 1 < self.cols and south_diagonal < self.rows:
                cell.southeast= self.grid[south_diagonal][col+1] 
    
    def background_colour_cell(self, cell):
        return (255,255,255,255)
    
    def to_png(self, size=10, fname="../examples/hex_maze.png"):
        
        a_size = size / 2
        b_size = (size * math.sqrt(3)) / 2
        width = size * 2
        height = b_size * 2
        
        img_width = int(3 * a_size * self.cols + a_size + 0.5)
        img_height = int(height * self.rows + b_size + 0.5)
        
        img = Image.new("RGBA",(img_width+2,img_height+2),(255,255,255,0))
        d = ImageDraw.Draw(img)
        wall = (0,0,0,255)
        for mode in ["background", "walls"]: # Draw background in first cycle, walls with second
            for cell in self.each_cell():
                # center point of cell
                cx = size + 3 * cell.col * a_size
                cy = b_size + cell.row * height
                
                if cell.col % 2 != 0:
                    cy += b_size
                
                # f/n = far/near
                # n/s/e/w = north/south/east/west
                x_fw = cx - size
                x_nw = cx - a_size
                x_ne = cx + a_size
                x_fe = cx + size
                
                # m = middle
                y_n = cy - b_size
                y_m = cy
                y_s = cy + b_size

                if mode == "background":
                    colour = self.background_colour_cell(cell)
                    if colour:
                        points = [(x_fw,y_m), (x_nw,y_n), (x_ne,y_n),
                                  (x_fe,y_m), (x_ne,y_s), (x_nw,y_s)]
                        d.polygon(xy=points,fill=colour)
                        
                else:
                    if not cell.southwest:
                        d.line([x_fw,y_m,x_nw,y_s], fill=wall,width=1)
                    if not cell.northwest:
                        d.line([x_fw,y_m,x_nw,y_n], fill=wall,width=1)
                    if not cell.north:
                        d.line([x_nw,y_n,x_ne,y_n], fill=wall,width=1)
                    if not cell.linked(cell.northeast):
                        d.line([x_ne,y_n,x_fe,y_m], fill=wall,width=1)
                    if not cell.linked(cell.southeast):
                        d.line([x_fe,y_m,x_ne,y_s], fill=wall,width=1)
                    if not cell.linked(cell.south):
                        d.line([x_ne,y_s,x_nw,y_s], fill=wall,width=1)
        img.save(fname,"PNG")  
        
if __name__ == "__main__":
    
    grid = HexGrid(10,10)
    rback = RecursiveBacktracker()
    rback.on(grid)
    
    grid.to_png(size=20,fname="../examples/rback_hex.png")
    print("Image created rback_hex.png")