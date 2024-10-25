import math
from PIL import Image, ImageDraw
from grid import Grid, Cell
import random
from recursive_backtracker import RecursiveBacktracker

class PolarCell(Cell):
    
    def __init__(self, row, column):
        super().__init__(row, column)
        self.outward = []
        self.cw, self.ccw, self.inward = None, None, None
        
    def neighbours(self):
        nei_list = []
        if self.cw:
            nei_list.append(self.cw)
        if self.ccw:
            nei_list.append(self.ccw)
        if self.inward:
            nei_list.append(self.inward)
        nei_list += self.outward
        
        return nei_list


class PolarGrid(Grid):
    def __init__(self, rows):
        super().__init__(rows, 1)
    
    def prepare_grid(self):
        rows = [None] * self.rows
        
        row_height = 1 / self.rows
        rows[0] = [PolarCell(0,0)]
        
        for rw in range(1,self.rows):
            radius = rw / self.rows
            circumference = 2 * math.pi * radius
            
            prev_count = len(rows[rw-1])
            est_cell_width = circumference / prev_count
            ratio = round(est_cell_width/row_height)
            cells = prev_count * ratio
            rows[rw] = [PolarCell(rw,col) for col in range(cells)]
        
        return rows
        
    def configure_cells(self):
       for cell in self.each_cell():
            row,col = cell.row, cell.col
            if row > 0:                                     
                if col + 1 >= len(self.grid[row]):
                    cell.cw = self.grid[row][col + 1 - len(self.grid[row])]
                else:
                   cell.cw = self.grid[row][col + 1] 
                if col - 1 < 0:
                   cell.ccw = self.grid[row][len(self.grid[row]) - 1]
                else:
                   cell.ccw = self.grid[row][col-1]

                ratio = len(self.grid[row]) / len(self.grid[row-1])
                parent = self.grid[row -1][round(col//ratio)]
                parent.outward.append(cell)
                cell.inward = parent
    
    def random_cell(self):
        row = random.randint(0, self.rows - 1)
        col = random.randint(0,len(self.grid[row]) - 1)
        
        return self.grid[row][col]
                
                
    
    
    def to_png(self, cell_size=25, fname="polar_grid.png"):
        img_size = 2 * self.rows * cell_size
        background = (255,255,255)
        wall = (0,0,0)
        
        img = Image.new("RGB",(img_size+5,img_size+5),background)
        d = ImageDraw.Draw(img)
        center = (img_size // 2) + 1
        
        for cell in self.each_cell():
            if cell.row == 0 :
                next
            theta = (2 * math.pi) / len(self.grid[cell.row])
            inner_radius = cell.row * cell_size
            outer_radius = (cell.row + 1) * cell_size
            theta_ccw = cell.col * theta
            theta_cw = (cell.col + 1) * theta
            
            ax = center + inner_radius * math.cos(theta_ccw)
            ay = center + inner_radius * math.sin(theta_ccw)
            bx = center + outer_radius * math.cos(theta_ccw)
            by = center + outer_radius * math.sin(theta_ccw)
            cx = center + inner_radius * math.cos(theta_cw)
            cy = center + inner_radius * math.sin(theta_cw)
            dx = center + outer_radius * math.cos(theta_cw)
            dy = center + outer_radius * math.sin(theta_cw)
            
            if not cell.linked(cell.inward) and (ax,ay) != (center,center):
                d.line([ax,ay,cx,cy], fill=wall,width=3)
            if not cell.linked(cell.cw) and  (cx,cy) != (center,center):
                d.line([cx,cy,dx,dy], fill=wall,width=3)
        
        d.circle((center,center), self.rows * cell_size,outline=wall,width=4)

        img.save(fname,"PNG")
        
if __name__ == "__main__":
    
    grid = PolarGrid(10)
    rback = RecursiveBacktracker()
    rback.on(grid)
    
    grid.to_png(cell_size=50,fname="rback_polar.png" )
    print("Image created polar_grid.png")