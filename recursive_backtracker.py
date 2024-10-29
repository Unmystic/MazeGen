# Implementation of Recurcive Backtracker algorithm for maze creation

import random
from grid import Grid, ColoredGrid
import os
from pathlib import Path
from wilsons import join_images

class RecursiveBacktracker(object):
    
    def on(self, grid, start_at = None):       
        if start_at is None :
            start_at = grid.random_cell()
        stack = []
        stack.append(start_at)
        
        while stack:
            current = stack[-1]
            neighbors = [nei for nei in current.neighbours() if not nei.links]
            
            if neighbors:
                neighbor = random.choice(neighbors)
                current.link(neighbor)
                stack.append(neighbor)
            else:
                stack.pop()
        
        return grid
    
def generate_colored_mazes(n=6):
    if not os.path.exists(os.path.abspath("examples/recursive_backtracker")):
        os.makedirs("examples/recursive_backtracker")
    
    path = Path("examples/recursive_backtracker")
    
    for i in range(n):
        grid = ColoredGrid(20,20)
        rback = RecursiveBacktracker()
        rback_grid = rback.on(grid)
        start =rback_grid.grid[rback_grid.rows // 2][rback_grid.cols // 2]
        
        rback_grid.set_distances(start.distances())
        fname = f"colored_maze_{i+1}.png"
        new_path = os.path.join(path , Path(fname))
        
        rback_grid.to_png(cell_size= 10, fname=new_path)
        print(f"Created image {fname} in directory {path}")


    
if __name__ == "__main__":
    grid = Grid(15,15)
    rback = RecursiveBacktracker()
    rback_grid = rback.on(grid)
    
    deadends = rback_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    rback_grid.braid(0.5)
    
    deadends = rback_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    
    print(rback_grid)
    
    rback_grid.to_png(cell_size=20, fname="recursive_backtracker.png")
    print("Created image recursive_backtracker.png")
    generate_colored_mazes()

    # Paths to your 6 images (adjust the paths as per your folder)
    image_paths = [
        "examples/recursive_backtracker/colored_maze_1.png", "examples/recursive_backtracker/colored_maze_2.png",
        "examples/recursive_backtracker/colored_maze_3.png","examples/recursive_backtracker/colored_maze_4.png",
        "examples/recursive_backtracker/colored_maze_5.png", "examples/recursive_backtracker/colored_maze_6.png"
    ]

    # Join the images
    combined_image = join_images(image_paths, space_between=10)

    # Save the result as a single image
    combined_image.save("examples/recursive_backtracker/combined_recursive_backtracker.png")
                