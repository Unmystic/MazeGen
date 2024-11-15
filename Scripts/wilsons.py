# Implementation of Wilsons algorithm

import random
from grid import Grid, ColoredGrid
import os
from pathlib import Path
from PIL import Image

class Wilsons(object):
    
    def on(self, grid):
        visited = set()
        unvisited = list(grid.each_cell())
        first = random.choice(unvisited)
        unvisited.remove(first)
        visited.add(first)
        
        while unvisited:
            cell = random.choice(unvisited)
            path = [cell]
            while cell not in visited:
                cell = random.choice(cell.neighbours())
                if cell in path:
                    position = path.index(cell)
                    path = path[:position+1]
                else:
                    path.append(cell)
            
            for i in range(len(path) - 1):
                path[i].link(path[i+1])
                unvisited.remove(path[i])
                visited.add(path[i])
        
        return grid

def generate_colored_mazes(n=6):
    if not os.path.exists(os.path.abspath("../examples/wilsons")):
        os.makedirs("../examples/wilsons")
    
    path = Path("../examples/wilsons")
    
    for i in range(n):
        grid = ColoredGrid(20,20)
        ws = Wilsons()
        ws_grid = ws.on(grid)
        start =ws_grid.grid[ws_grid.rows // 2][ws_grid.cols // 2]
        
        ws_grid.set_distances(start.distances())
        fname = f"colored_maze_{i+1}.png"
        new_path = os.path.join(path , Path(fname))
        
        ws_grid.to_png(cell_size= 10, fname=new_path)
        print(f"Created image {fname} in directory {path}")


# Function to join 6 images in two rows with 3 images per row and spaces between them
def join_images(image_paths, space_between=10):
    # Open all the images and store them in a list
    images = [Image.open(img_path) for img_path in image_paths]

    # Get the size of a single image (assuming all images have the same size)
    img_width, img_height = images[0].size

    # Calculate the size of the new image (3 images per row + spaces)
    total_width = 3 * img_width + 2 * space_between
    total_height = 2 * img_height + space_between

    # Create a new blank image with a white background
    new_image = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 0))

    # Paste the images into the new image
    for i, img in enumerate(images):
        x_offset = (i % 3) * (img_width + space_between)
        y_offset = (i // 3) * (img_height + space_between)
        new_image.paste(img, (x_offset, y_offset))

    return new_image




if __name__ == "__main__":
    
    grid = Grid(25,25)
    ws = Wilsons()
    ws_grid = ws.on(grid)
    
    deadends = ws_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    
    ws_grid.to_png(cell_size=20, fname="../examples/wilsons.png")
    print("Created image wilsons.png")
    generate_colored_mazes()
    
    # Paths to your 6 images (adjust the paths as per your folder)
    image_paths = [
        "../examples/wilsons/colored_maze_1.png", "../examples/wilsons/colored_maze_2.png",
        "../examples/wilsons/colored_maze_3.png","../examples/wilsons/colored_maze_4.png",
        "../examples/wilsons/colored_maze_5.png", "../examples/wilsons/colored_maze_6.png"
    ]

    # Join the images
    combined_image = join_images(image_paths, space_between=10)

    # Save the result as a single image
    combined_image.save("../examples/wilsons/combined_wilsons.png")