import random
from PIL import Image, ImageDraw
from distances import Distances

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
    
    # Retrieve all connection to current cell
    def linkslist(self):
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
    
    # Calculate distances to current cell
    def distances(self):
        distances = Distances(self)
        frontier = [self]
        visited = set()
        # print(self, distances.get_cell_distance(self))
        visited.add(self)
        while frontier:
            new_frontier = []
            for cell in frontier:
                for linked in cell.links.keys():
                    if linked not in visited:
                        distances.cells[linked] = distances.cells[cell] + 1
                        new_frontier.append(linked)
                        visited.add(linked)
            frontier = new_frontier
        return distances


class Grid(object):
    def __init__(self,rows,columns):
        self.rows = rows
        self.cols = columns
        self.grid = self.prepare_grid()
        self.configure_cells()
        
    def contents_of(self,cell):
        return "   "
        
    def __str__(self):
        output =  "+" + "---+" * self.cols + "\n"
        for row in self.grid:
            top = "|"
            bottom = "+"
            for cell in row:
                body = f"{self.contents_of(cell)}"
                
                if cell and cell.linked(cell.east):
                    body += " "
                else:
                    body += "|"
                top += body
                if cell and cell.linked(cell.south):
                    bottom += "   +"
                else:
                    bottom += "---+"
            top += "\n"
            bottom += "\n"
            output += top
            output += bottom
                
                    
        return output
        
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
        for cell in self.each_cell():
            row, col = cell.row, cell.col
            
            if row - 1 >= 0:
                cell.north = self.grid[row-1][col]
            if col - 1 >= 0:
                cell.west = self.grid[row][col-1]
            if row + 1 < self.rows:
                cell.south = self.grid[row+1][col]
            if col + 1 < self.cols:
                cell.east = self.grid[row][col+1]            
            
        # Previous implementation(delete)
        # for i in range(self.rows):
        #     for j in range(self.cols):
        #         cell = self.grid[i][j]                             
        #         if i - 1 >= 0:
        #             cell.north = self.grid[i-1][j]
        #         if j - 1 >= 0:
        #             cell.west = self.grid[i][j-1]
        #         if i + 1 < self.rows:
        #             cell.south = self.grid[i+1][j]
        #         if j + 1 < self.cols:
        #             cell.east = self.grid[i][j+1]     
    
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
                
    def background_colour_cell(self, cell):
        return None
    
    def to_png(self,cell_size=25,inset=0, fname="maze.png"):
        img_width = cell_size * self.cols
        img_height = cell_size * self.rows
        inset = int(cell_size * inset)
        
        img = Image.new("RGB",(img_width+2,img_height+2),(255,255,255))
        d = ImageDraw.Draw(img)
        wall = (0,0,0)
        for mode in ["background", "walls"]: # Draw background in first cycle, walls with second
            for cell in self.each_cell():
                x = cell.col * cell_size
                y = cell.row * cell_size
                
                if inset > 0:
                    self.to_png_with_inset(img, d, cell, mode,cell_size, wall,x,y,inset)
                else:
                    self.to_png_without_inset(img, d, cell, mode,cell_size, wall,x,y)
                
        img.save(fname,"PNG")
    
    def to_png_without_inset(self, img, d, cell, mode,cell_size, wall,x,y):
        x1, y1 = x, y
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        
        if mode == "background":
            colour = self.background_colour_cell(cell)
            if colour:
                d.rectangle([x1,y1,x2,y2], fill=colour) 
        else:
            if not cell.north:
                d.line([x1,y1,x2,y1], fill=wall,width=2)
            if not cell.west:
                d.line([x1,y1,x1,y2], fill=wall,width=2)
            if not cell.linked(cell.east):
                d.line([x2,y1,x2,y2], fill=wall,width=2)
            if not cell.linked(cell.south):
                d.line([x1,y2,x2,y2], fill=wall,width=2)
                
    def cell_coordinates_with_inset(self,x,y,cell_size,inset):
        x1,x4 = x , x + cell_size
        x2 = x1 + inset
        x3 = x4 - inset
        
        y1, y4 = y, y + cell_size
        y2 = y1 + inset
        y3 = y4 - inset
        
        return [x1,x2,x3,x4,y1,y2,y3,y4]
    
    def to_png_with_inset(self,img, d, cell, mode,cell_size, wall,x,y,inset):
        x1,x2,x3,x4,y1,y2,y3,y4 = self.cell_coordinates_with_inset(x,y,cell_size,inset)
        
        if mode == "background":
            pass
            #TODO
        else:
            width = 1
            if cell.linked(cell.north):
                d.line([x2,y1,x2,y2], fill=wall,width=width)
                d.line([x3,y1,x3,y2], fill=wall,width=width)
            else:
                d.line([x2,y2,x3,y2], fill=wall,width=width)
                
            if cell.linked(cell.south):
                d.line([x2,y3,x2,y4], fill=wall,width=width)
                d.line([x3,y3,x3,y4], fill=wall,width=width)
            else:
                d.line([x2,y3,x3,y3], fill=wall,width=width)
                
            if cell.linked(cell.west):
                d.line([x1,y2,x2,y2], fill=wall,width=width)
                d.line([x1,y3,x2,y3], fill=wall,width=width)
            else:
                d.line([x2,y2,x2,y3], fill=wall,width=width)
                
            if cell.linked(cell.east):
                d.line([x3,y2,x4,y2], fill=wall,width=width)
                d.line([x3,y3,x4,y3], fill=wall,width=width)
            else:
                d.line([x3,y2,x3,y3], fill=wall,width=width)
        
    
    def deadends(self):
        deadends = []
        for cell in self.each_cell():
            if len(cell.links) == 1:
                deadends.append(cell)
        return deadends
    
    def braid(self, p = 1.0):
        
        if p >1.0 or p < 0 :
            raise TypeError(" Parameter -p- must be a float between 0 and 1")
        
        deadends = self.deadends()
        random.shuffle(deadends)
        
        for cell in deadends:
            if len(cell.links) != 1 or random.random() > p:
                next
                neigbors = [nei for nei in cell.neighbours() if not cell.linked(nei)]              
                best = [nei for nei in neigbors if len(nei.links) == 1]
                if not best:
                    best = neigbors
                nei = random.choice(best)
                cell.link(nei)

class DistanceGrid(Grid):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.distances = {}
    
    def contents_of(self, cell):
        # print(self.distances)
        if self.distances and cell in self.distances:
            d = str(self.distances[cell])
            if len(d) == 1:
                return " " + d + " "
            elif len(d) == 2:
                return " " + d
            elif len(d) == 3:
                return d
            else:
                return "big"
                
            #return self.to_base(self.distances[cell],36)
        else:
            return "   "
    
    def to_base(self, number, base):
        base_string = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""
        while number:
            result += base_string[number % base]
            number //= base
        return result[::-1] or "0"     

class ColoredGrid(Grid):
    
    def set_distances(self, distances):
        self.distances = distances.cells
        self.max_dist = max(self.distances.values())    
    
    def background_colour_cell(self, cell):
        if cell in self.distances: 
            distance = self.distances[cell]
            intensity = (self.max_dist - distance) / self.max_dist
            dark = int(255*intensity)
            bright = 128 + int(127*intensity)
            return (dark,bright,dark)
            
        else: 
            return None
        
class MaskedGrid(Grid):
    
    def __init__(self, mask):
        self.mask = mask
        self.rows = mask.rows
        self.cols = mask.columns
        super().__init__(mask.rows, mask.columns)
    
        
    def prepare_grid(self):
        grid = []
        for i in range(self.rows):
            row_list = []
            for j in range(self.cols):
                if self.mask.bits[i][j]:
                    Cell(i,j)
                    row_list.append(Cell(i,j))
                else:
                    row_list.append(None)
            grid.append(row_list)
        #print(grid)
        return grid
    
    def configure_cells(self):
        for cell in self.each_cell():
            if cell:
                row, col = cell.row, cell.col
                
                if row - 1 >= 0 and self.mask.bits[row-1][col]:
                    cell.north = self.grid[row-1][col]
                if col - 1 >= 0 and self.mask.bits[row][col-1]:
                    cell.west = self.grid[row][col-1]
                if row + 1 < len(self.grid) and self.mask.bits[row+1][col]:
                    cell.south = self.grid[row+1][col]
                if col + 1 < len(self.grid[row]) and self.mask.bits[row][col+1]:
                    cell.east = self.grid[row][col+1]      
    
    def background_colour_cell(self, cell):
        return (255,255,255,255)
    
    def to_png(self,cell_size=25, fname="maze.png"):
        img_width = cell_size * self.cols
        img_height = cell_size * self.rows
        
        img = Image.new("RGBA",(img_width+2,img_height+2),(255,255,255,0))
        d = ImageDraw.Draw(img)
        wall = (0,0,0,255)
        for mode in ["background", "walls"]: # Draw background in first cycle, walls with second
            for cell in self.each_cell():
                if cell:
                    x1 = cell.col * cell_size
                    y1 = cell.row * cell_size
                    x2 = (cell.col +1) * cell_size
                    y2 = (cell.row +1) * cell_size
                    if mode == "background":
                        colour = self.background_colour_cell(cell)
                        if colour:
                            d.rectangle([x1,y1,x2,y2], fill=colour) 
                    else:
                        if not cell.north:
                            d.line([x1,y1,x2,y1], fill=wall,width=2)
                        if not cell.west:
                            d.line([x1,y1,x1,y2], fill=wall,width=2)
                        if not cell.linked(cell.east):
                            d.line([x2,y1,x2,y2], fill=wall,width=2)
                        if not cell.linked(cell.south):
                            d.line([x1,y2,x2,y2], fill=wall,width=2)
        img.save(fname,"PNG")
    
    def random_cell(self):
        row, col = self.mask.random_location()
        
        return self.grid[row][col]
    
    def size(self):
        return self.mask.count()
        
    
if __name__ == "__main__":
    
    grid = Grid(8,8)
    start = grid.grid[0][0]
    distances = start.distances()
    print(grid)
    
               
            
        