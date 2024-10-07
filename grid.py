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
                
                if cell.linked(cell.east):
                    body += " "
                else:
                    body += "|"
                top += body
                if cell.linked(cell.south):
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
    
    def to_png(self,cell_size=25):
        img_width = cell_size * self.cols
        img_height = cell_size * self.rows
        
        img = Image.new("RGB",(img_width+1,img_height+1),(255,255,255))
        d = ImageDraw.Draw(img)
        wall = (0,0,0)
        for cell in self.each_cell():
            x1 = cell.col * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.col +1) * cell_size
            y2 = (cell.row +1) * cell_size
            if not cell.north:
                d.line([x1,y1,x2,y1], fill=wall,width=2)
            if not cell.west:
                d.line([x1,y1,x1,y2], fill=wall,width=2)
            if not cell.linked(cell.east):
                d.line([x2,y1,x2,y2], fill=wall,width=2)
            if not cell.linked(cell.south):
                d.line([x1,y2,x2,y2], fill=wall,width=2)
        img.save("maze_16x32.png","PNG")

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
            
    
if __name__ == "__main__":
    
    grid = Grid(8,8)
    # print(grid.grid)
    # rand_cell = grid.random_cell()
    # print([rand_cell.row, rand_cell.col], rand_cell.neighbours())
    # print(grid.size())
    # print(list(grid.each_row()))
    # print(list(grid.each_cell()))
    # grid.to_png()
    start = grid.grid[0][0]
    distances = start.distances()
    print(grid)
    
               
            
        