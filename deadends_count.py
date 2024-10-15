from grid import Grid
from binaryTree import BinaryTree
from sidewinder import Sidewinder
from ald_bro import AldousBroder
from wilsons import Wilsons
from hunt_and_kill import HuntandKill
from recursive_backtracker import RecursiveBacktracker

algorithms = [BinaryTree(), Sidewinder(), AldousBroder(), Wilsons(), HuntandKill(), RecursiveBacktracker()]

tries = 100
size = 20
averages = {}

for algorithm in algorithms:
    print(f"running {type(algorithm).__name__}...")
    
    deadends_count = []
    for i in range(tries):
        grid = Grid(size,size)
        algorithm.on(grid)
        deadends_count.append(len(grid.deadends()))
    averages[type(algorithm).__name__] = round(sum(deadends_count) // 100)
    
total_cells = size * size
print("")
print(f"Average dead-ends per {size}x{size} maze of {total_cells} cells:")
print("")

sorted_averages = sorted(averages,key=averages.get, reverse=True)

for algo in sorted_averages:
    percentage = round((averages[algo] *100) / total_cells)
    print('{:>20s} : {:>3d}/{:d} ({:d}%)'.format(algo,averages[algo],total_cells,percentage))
        