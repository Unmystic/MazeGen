

class Distances(object):
    def __init__(self, root):
        self.root = root
        self.cells = {}
        self.cells[root] = 0
    
    def get_cell_distance(self,cell):
        return self.cells[cell]
    
    def set_cell_distance(self,cell,distance):
        self.cells[cell] = distance
        
    def cells(self):
        return self.cells.keys()
    
    def path_to_goal(self, goal):
        current = goal
        
        breadcrumbs = Distances(self.root)
        breadcrumbs.cells[current] = self.cells[current]
        
        while current != self.root:
            for neighbor in current.links.keys():
                if self.cells[neighbor] < self.cells[current]:
                    breadcrumbs.cells[neighbor] = self.cells[neighbor]
                    current = neighbor
                    break
        return breadcrumbs.cells
                