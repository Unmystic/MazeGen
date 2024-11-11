from grid import Grid, Cell, ColoredGrid
import random
import os
from pathlib import Path
from sidewinder import Sidewinder
from PIL import Image

class Ellers(object):

    class RowState(object):
        def __init__(self,starting_set=0):
            self.cells_in_set = {}
            self.set_for_cell = {} 
            self.next_set = starting_set
        
        def record(self,set,cell):

            self.set_for_cell[cell.col] = set

            if set not in self.cells_in_set:
                self.cells_in_set[set] = []
            
            self.cells_in_set[set].append(cell)
        
        def set_for(self,cell):
            if cell.col not in self.set_for_cell:
                self.record(self.next_set, cell)
                self.next_set += 1
            
            return self.set_for_cell[cell.col]
        
        def merge(self, winner, loser):

            for cell in self.cells_in_set[loser]:
                self.set_for_cell[cell.col] = winner
                self.cells_in_set[winner].append(cell)

            self.cells_in_set.pop(loser)

        def next_row(self):
            return Ellers.RowState(self.next_set)

        def each_set(self):
            for set,cells in self.cells_in_set.items():
                yield set, cells 
    
    def on(self, grid):

        row_state = Ellers.RowState()

        for row in grid.each_row():
            for cell in row:
                if not cell.west:
                    pass
                else:
                    set = row_state.set_for(cell)
                    prior_set = row_state.set_for(cell.west)
                    if set != prior_set and (cell.south is None or random.randint(0,1) == 0):
                        should_link = True
                    else:
                        should_link = False
                    
                    if should_link:
                        cell.link(cell.west)
                        row_state.merge(prior_set,set)
            
            if row[0].south:
                next_row = row_state.next_row()

                for set, cells in row_state.each_set():
                    random.shuffle(cells)
                    for id,cell in enumerate(cells) :
                        if id == 0 or random.randint(0,2) == 0:
                            cell.link(cell.south)
                            next_row.record(row_state.set_for(cell), cell.south)
                
                row_state = next_row
        return grid

def generate_colored_mazes_comparison(n=1):
    if not os.path.exists(os.path.abspath("examples/ellers_vs_sidewinder")):
        os.makedirs("examples/ellers_vs_sidewinder")
    
    path = Path("examples/ellers_vs_sidewinder")
    
    for i in range(n):
        grid = ColoredGrid(20,20)
        ellers = Ellers()
        ellers_grid = ellers.on(grid)  
        start =ellers_grid.grid[ellers_grid.rows // 2][ellers_grid.cols // 2]
        
        ellers_grid.set_distances(start.distances())
        fname = f"colored_maze_{i+1}.png"
        new_path = os.path.join(path , Path(fname))
        
        ellers_grid.to_png(cell_size= 20, fname=new_path)
        print(f"Created image {fname} in directory {path}")

    for i in range(n):
        grid = ColoredGrid(20,20)
        sidew = Sidewinder()
        sgrid = sidew.on(grid)  
        start =sgrid.grid[sgrid.rows // 2][sgrid.cols // 2]
        
        sgrid.set_distances(start.distances())
        fname = f"colored_maze_{i+2}.png"
        new_path = os.path.join(path , Path(fname))
        
        sgrid.to_png(cell_size= 20, fname=new_path)
        print(f"Created image {fname} in directory {path}")

def join_two_images(image_paths, space_between=10):
    # Open all the images and store them in a list
    images = [Image.open(img_path) for img_path in image_paths]

    # Get the size of a single image (assuming all images have the same size)
    img_width, img_height = images[0].size

    # Calculate the size of the new image (2 images + space)
    total_width = 2 * img_width + space_between
    total_height = img_height + space_between

    # Create a new blank image with a white background
    new_image = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 0))

    # Paste the images into the new image
    for i, img in enumerate(images):
        x_offset = (i % 3) * (img_width + space_between)
        y_offset = (i // 3) * (img_height + space_between)
        new_image.paste(img, (x_offset, y_offset))

    return new_image

if __name__ == "__main__":
    
    grid = Grid(20,20)
    ellers = Ellers()
    ellers_grid = ellers.on(grid)  
    fname = "examples/ellers_maze.png"
    ellers_grid.to_png(cell_size=20,fname=fname)
    print(f"Created image {fname}")

    generate_colored_mazes_comparison()
    # Paths to your 6 images (adjust the paths as per your folder)
    image_paths = [
        "examples/ellers_vs_sidewinder/colored_maze_1.png", "examples/ellers_vs_sidewinder/colored_maze_2.png",
     ]
    # Join the images
    combined_image = join_two_images(image_paths, space_between=10)
    # Save the result as a single image
    combined_image.save("examples/ellers_vs_sidewinder/ellers_vs_sidewinder.png")