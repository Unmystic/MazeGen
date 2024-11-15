from grid import Cell, Grid
import random


class BinaryTree(object):
    
    def on(self, grid):
        for cell in grid.each_cell():
            neighbors = []
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)
            
            if neighbors:            
                neighbor = random.choice(neighbors)
                cell.link(neighbor)
        return grid
    

if __name__ == "__main__":
    grid = Grid(8,8)
    tree = BinaryTree()
    print(tree.on(grid))