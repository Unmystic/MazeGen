

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