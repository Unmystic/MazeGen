# Implementation of "Hunt and Kill" algorithm for maze creation

import random
from grid import Grid, ColoredGrid
import os
from pathlib import Path
from wilsons import join_images

class HuntandKill(object):
    
    def on(self, grid):
        current = grid.random_cell()
        
        while current:
            unvisited_neighbors = [nei for nei in current.neighbours() if not nei.links]
            
            if unvisited_neighbors:
                neigbor = random.choice(unvisited_neighbors)
                current.link(neigbor)
                current = neigbor
            else:
                current = None
                
                for cell in grid.each_cell():
                    visited_neighbors = [nei for nei in cell.neighbours() if nei.links]
                    if not cell.links and visited_neighbors:
                        current = cell
                        neigbor = random.choice(visited_neighbors)
                        current.link(neigbor)
                        break
        return grid

def generate_colored_mazes(n=6):
    if not os.path.exists(os.path.abspath("examples/hunt_and_kill")):
        os.makedirs("examples/hunt_and_kill")
    
    path = Path("examples/hunt_and_kill")
    
    for i in range(n):
        grid = ColoredGrid(20,20)
        hak = HuntandKill()
        hak_grid = hak.on(grid)
        start =hak_grid.grid[hak_grid.rows // 2][hak_grid.cols // 2]
        
        hak_grid.set_distances(start.distances())
        fname = f"colored_maze_{i+1}.png"
        new_path = os.path.join(path , Path(fname))
        
        hak_grid.to_png(cell_size= 10, fname=new_path)
        print(f"Created image {fname} in directory {path}")


    
if __name__ == "__main__":
    grid = Grid(25,25)
    hak = HuntandKill()
    hak_grid = hak.on(grid)
    hak_grid.to_png(cell_size=20, fname="hunt_and_kill.png")
    print("Created image hunt_and_kill.png")
    generate_colored_mazes()

    # Paths to your 6 images (adjust the paths as per your folder)
    image_paths = [
        "examples/hunt_and_kill/colored_maze_1.png", "examples/hunt_and_kill/colored_maze_2.png",
        "examples/hunt_and_kill/colored_maze_3.png","examples/hunt_and_kill/colored_maze_4.png",
        "examples/hunt_and_kill/colored_maze_5.png", "examples/hunt_and_kill/colored_maze_6.png"
    ]

    # Join the images
    combined_image = join_images(image_paths, space_between=10)

    # Save the result as a single image
    combined_image.save("examples/hunt_and_kill/combined_hunt_and_kill.png")
                