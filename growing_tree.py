from grid import Grid, Cell, ColoredGrid
import random
import os
from pathlib import Path
from wilsons import join_images
import heapq

class GrowingTree(object):
    def on(self, grid, start_at=None, func = None):
        if start_at is None:
            start_at = grid.random_cell()
        
        if func is None:
            func = last_cell
        active = [start_at]
        
        while active:
            cell = func(active)
            available_neighbors = [nei for nei in cell.neighbours() if not nei.links]
            
            if available_neighbors:
                nei = random.choice(available_neighbors)
                cell.link(nei)
                active.append(nei)
            else:
                active.remove(cell)
        return grid

def random_cell(cell_list):
    return random.choice(cell_list)

def last_cell(cell_list):
    return cell_list[-1]

def mixed_choice(cell_list):
    if random.randint(0,1) == 0:
        return cell_list[-1]
    else:
        return random.choice(cell_list)
    
if __name__ == "__main__":
    
    grid = Grid(20,20)
    gtree = GrowingTree()
    random_rtree_grid = gtree.on(grid,func=random_cell)  
    fname = "examples/random_rtree_maze.png"
    random_rtree_grid.to_png(cell_size=20,fname=fname)
    print(f"Created image {fname}")
    
    grid = Grid(20,20)
    gtree = GrowingTree()
    last_rtree_grid = gtree.on(grid, func=last_cell)  
    fname = "examples/last_rtree_maze.png"
    last_rtree_grid.to_png(cell_size=20,fname=fname)
    print(f"Created image {fname}")
    
    grid = Grid(20,20)
    gtree = GrowingTree()
    mixed_rtree_grid = gtree.on(grid,func=mixed_choice)  
    fname = "examples/mixed_rtree_maze.png"
    mixed_rtree_grid.to_png(cell_size=20,fname=fname)
    print(f"Created image {fname}")