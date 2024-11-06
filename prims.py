from grid import Grid, Cell, ColoredGrid
import random
import os
from pathlib import Path
from wilsons import join_images
import heapq

class SimplifiedPrims(object):
    
    def on(self, grid, start_at=None):
        if start_at is None:
            start_at = grid.random_cell()
        
        active = [start_at]
        
        while active:
            cell = random.choice(active)
            available_neighbors = [nei for nei in cell.neighbours() if not nei.links]
            
            if available_neighbors:
                nei = random.choice(available_neighbors)
                cell.link(nei)
                active.append(nei)
            else:
                active.remove(cell)
        return grid

class TruePrims(object):
    
    def on(self, grid, start_at=None):
        if start_at is None:
            start_at = grid.random_cell()
        
        costs = {}     
        for cell in grid.each_cell():
            costs[cell] = random.randint(1,100)
        counter = 0    
        active = [(costs[start_at], counter, start_at)]
        heapq.heapify(active)
        
        while active:
            cost, count, cell = heapq.heappop(active)
            available_neighbors = []
            id_num = 0
            for nei in cell.neighbours():
                if not nei.links:
                    available_neighbors.append([costs[nei], id_num, nei])
                    id_num += 1
            available_neighbors.sort()
            
            if available_neighbors:
                nei = available_neighbors.pop(0)[2]
                cell.link(nei)
                heapq.heappush(active, (cost, count, cell) )
                counter += 1
                heapq.heappush(active, (costs[nei], counter, nei) )

        return grid

def generate_colored_mazes_s(n=6):
    if not os.path.exists(os.path.abspath("examples/prims/simplified_prims")):
        os.makedirs("examples/prims/simplified_prims")
    
    path = Path("examples/prims/simplified_prims")
    
    for i in range(n):
        grid = ColoredGrid(20,20)
        sprims = SimplifiedPrims()
        sprims_grid = sprims.on(grid) 
        start =sprims_grid.grid[sprims_grid.rows // 2][sprims_grid.cols // 2]
        
        sprims_grid.set_distances(start.distances())
        fname = f"colored_maze_{i+1}.png"
        new_path = os.path.join(path , Path(fname))
        
        sprims_grid.to_png(cell_size= 10, fname=new_path)
        print(f"Created image {fname} in directory {path}")

def generate_colored_mazes(n=6):
    if not os.path.exists(os.path.abspath("examples/prims/true_prims")):
        os.makedirs("examples/prims/true_prims")
    
    path = Path("examples/prims/true_prims")
    
    for i in range(n):
        grid = ColoredGrid(20,20)
        prims = TruePrims()
        prims_grid = prims.on(grid) 
        start =prims_grid.grid[prims_grid.rows // 2][prims_grid.cols // 2]
        
        prims_grid.set_distances(start.distances())
        fname = f"colored_maze_{i+1}.png"
        new_path = os.path.join(path , Path(fname))
        
        prims_grid.to_png(cell_size= 10, fname=new_path)
        print(f"Created image {fname} in directory {path}")
    
    
if __name__ == "__main__":
    
    # grid = Grid(20,20)
    # sprims = SimplifiedPrims()
    # sprims_grid = sprims.on(grid) 
    
    # deadends = sprims_grid.deadends()
    # print(f"The maze has {len(deadends)} deadends")
    # # sprims_grid.braid(0.3)
    # # deadends = sprims_grid.deadends()
    # # print(f"The maze has {len(deadends)} deadends")
    
    # fname = "simple_prims_maze.png"
    # sprims_grid.to_png(cell_size=20,fname=fname)
    # print(f"Created image {fname}")
    
    # generate_colored_mazes_s()
    # # Paths to your 6 images (adjust the paths as per your folder)
    # image_paths = [
    #     "examples/prims/simplified_prims/colored_maze_1.png", "examples/prims/simplified_prims/colored_maze_2.png",
    #     "examples/prims/simplified_prims/colored_maze_3.png", "examples/prims/simplified_prims/colored_maze_4.png",
    #     "examples/prims/simplified_prims/colored_maze_5.png", "examples/prims/simplified_prims/colored_maze_6.png"
    # ]
    # # Join the images
    # combined_image = join_images(image_paths, space_between=10)
    # # Save the result as a single image
    # combined_image.save("examples/prims/simplified_prims/combined_s_prims.png")
    
    grid = Grid(20,20)
    prims = TruePrims()
    prims_grid = prims.on(grid) 
    
    deadends = prims_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    # sprims_grid.braid(0.3)
    # deadends = sprims_grid.deadends()
    # print(f"The maze has {len(deadends)} deadends")
    
    fname = "true_prims_maze.png"
    prims_grid.to_png(cell_size=20,fname=fname)
    print(f"Created image {fname}")
    
    generate_colored_mazes()
    # Paths to your 6 images (adjust the paths as per your folder)
    image_paths = [
        "examples/prims/true_prims/colored_maze_1.png", "examples/prims/true_prims/colored_maze_2.png",
        "examples/prims/true_prims/colored_maze_3.png", "examples/prims/true_prims/colored_maze_4.png",
        "examples/prims/true_prims/colored_maze_5.png", "examples/prims/true_prims/colored_maze_6.png"
    ]
    # Join the images
    combined_image = join_images(image_paths, space_between=10)
    # Save the result as a single image
    combined_image.save("examples/prims/true_prims/combined_t_prims.png")