from grid import Cell, Grid
import random


class Sidewinder(object):
    
    def on(self, grid):
        for row in grid.each_row():
            run = []
            for cell in row:
                run.append(cell)
                if not cell.east:
                    at_eastern_border = True
                else:
                    at_eastern_border = False
                if not cell.north:
                    at_northern_border = True
                else:
                    at_northern_border = False
                
                should_close_out = (at_eastern_border or
                (not at_northern_border and random.randint(0,2) == 0))
                if should_close_out:
                    member = random.choice(run)
                    if member.north:
                        member.link(member.north)
                    run.clear()
                else:
                    cell.link(cell.east)
        return grid
    
if __name__ == "__main__":
    grid = Grid(16,32)
    sdw = Sidewinder()
    res = sdw.on(grid)
    print(res)
    res.to_png()