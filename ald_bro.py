# Implementation of Aldous-Broder algorithm, creating random walks
import random
from grid import Grid, ColoredGrid
import os
from pathlib import Path
from wilsons import join_images


class AldousBroder(object):
    
    def on(self, grid):
        cell = grid.random_cell()
        unvisited = grid.size() - 1
        
        while unvisited > 0 :
            neighbor = random.choice(cell.neighbours())
            if not neighbor.links :
                cell.link(neighbor)
                unvisited -= 1
            cell = neighbor
        
        return grid

def generate_colored_mazes(n=6):
    if not os.path.exists(os.path.abspath("examples/aldous_broder")):
        os.makedirs("examples/aldous_broder")
    
    path = Path("examples/aldous_broder")
    
    for i in range(n):
        grid = ColoredGrid(20,20)
        ab = AldousBroder()
        ab_grid = ab.on(grid)
        start =ab_grid.grid[ab_grid.rows // 2][ab_grid.cols // 2]
        
        ab_grid.set_distances(start.distances())
        fname = f"colored_maze_{i+1}.png"
        new_path = os.path.join(path , Path(fname))
        
        ab_grid.to_png(cell_size= 10, fname=new_path)
        print(f"Created image {fname} in directory {path}")

    
    
if __name__ == "__main__":
    
    grid = Grid(25,25)
    ab = AldousBroder()
    ab_grid = ab.on(grid)
    
    ab_grid.to_png(cell_size=20, fname="aldous_broder.png")
    generate_colored_mazes()
    
    # Paths to your 6 images (adjust the paths as per your folder)
    image_paths = [
        "examples/aldous_broder/colored_maze_1.png", "examples/aldous_broder/colored_maze_2.png",
        "examples/aldous_broder/colored_maze_3.png","examples/aldous_broder/colored_maze_4.png",
        "examples/aldous_broder/colored_maze_5.png", "examples/aldous_broder/colored_maze_6.png"
    ]

    # Join the images
    combined_image = join_images(image_paths, space_between=10)

    # Save the result as a single image
    combined_image.save("examples/aldous_broder/combined_image.png")