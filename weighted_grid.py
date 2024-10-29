import math
from PIL import Image, ImageDraw
from grid import Grid, Cell
import random
from recursive_backtracker import RecursiveBacktracker
import heapq
from distances import Distances

class WeightedCell(Cell):
    
    def __init__(self, row, column):
        super().__init__(row, column)
        self.weight = 1
        
    def distances(self):
        weights = Distances(self)
        count_order = 0
        pending = [(0,count_order,self)]
        heapq.heapify(pending)
        
        while pending:
            wei,_value, currcell = heapq.heappop(pending)
            for nei in currcell.linkslist():
                total_weight = wei + nei.weight
                if nei not in weights.cells or total_weight < weights.cells[nei]:
                    weights.cells[nei] = total_weight
                    count_order+= 1
                    heapq.heappush(pending, (total_weight,count_order,nei))
        return weights
    

class WeightedGrid(Grid):
    
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.distances = {}

    def set_distances(self,distances):     
        if isinstance(distances, dict):
            self.distances = distances
        else:
            self.distances = distances.cells
        self.max_dist = max(self.distances.values())    
    
    def prepare_grid(self):
        grid = []
        for i in range(self.rows):
            row_list = []
            for j in range(self.cols):
                Cell(i,j)
                row_list.append(WeightedCell(i,j))
            grid.append(row_list)
        return grid
    
    def background_colour_cell(self, cell):
        if cell.weight > 1:
            return (255, 0, 0)
        elif cell in self.distances: 
            distance = self.distances[cell]
            intensity = 64 + 191*(self.max_dist - distance) / self.max_dist

            return (int(intensity),int(intensity),0)
            
        else: 
            return None
                    
                    
if __name__ == "__main__":
    
    grid = WeightedGrid(15,15)
    rback = RecursiveBacktracker()
    rback_grid = rback.on(grid)
    
    deadends = rback_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    rback_grid.braid(0.5)
    
    deadends = rback_grid.deadends()
    print(f"The maze has {len(deadends)} deadends")
    
    start, finish = rback_grid.grid[0][0], rback_grid.grid[rback_grid.rows - 1][rback_grid.cols - 1]
    distances = start.distances()
    rback_grid.set_distances(distances.path_to_goal(finish))
    
    rback_grid.to_png(cell_size=20, fname="weighted_rback.png")
    print("Created image weighted_rback.png")
    
    lava = random.choice(list(rback_grid.distances.keys()))
    lava.weight = 50
    
    distances = start.distances()
    rback_grid.set_distances(distances.path_to_goal(finish))
    rback_grid.to_png(cell_size=20, fname="weighted_rback_rerouted.png")
    print("Created image weighted_rback_rerouted.png")
    
    