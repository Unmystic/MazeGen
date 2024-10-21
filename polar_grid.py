import math
from PIL import Image, ImageDraw
from grid import Grid


class PolarGrid(Grid):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
    
    def to_png(self, cell_size=25, fname="polar_grid.png"):
        img_size = 2 * self.rows * cell_size
        background = (255,255,255)
        wall = (0,0,0)
        
        img = Image.new("RGB",(img_size+5,img_size+5),background)
        d = ImageDraw.Draw(img)
        center = (img_size // 2) + 1
        
        for cell in self.each_cell():
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
            
            if not cell.linked(cell.north):
                d.line([ax,ay,cx,cy], fill=wall,width=2)
            if not cell.linked(cell.east):
                d.line([cx,cy,dx,dy], fill=wall,width=2)
        
        d.circle((center,center), self.rows * cell_size,outline=wall,width=2)

        img.save(fname,"PNG")
        
if __name__ == "__main__":
    
    grid = PolarGrid(8,8)
    
    grid.to_png(cell_size=30)
    print("Image created polar_grid.png")