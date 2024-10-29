import math
from PIL import Image, ImageDraw
from grid import Grid, Cell
import random
from recursive_backtracker import RecursiveBacktracker
import heapq
from distances import Distances


class OverCell(Cell):
    def __init__(self, row, column, grid):
        super().__init__(row, column)
        self.grid = grid
    
    def neighbours(self):
        nei =  super().neighbours()
        
        if self.can_tunnel_north():
            nei.append(self.north.north)
        if self.can_tunnel_south():
            nei.append(self.south.south)
        if self.can_tunnel_west():
            nei.append(self.west.west)
        if self.can_tunnel_east():
            nei.append(self.east.east)
        return nei
    
    def can_tunnel_north(self):
        if self.north and self.north.north and self.north.horizontal_passage():
            return True
        else:
            return False
        
    def can_tunnel_south(self):
        if self.south and self.south.south and self.south.horizontal_passage():
            return True
        else:
            return False
    def can_tunnel_west(self):
        if self.west and self.west.west and self.west.vertical_passage():
            return True
        else:
            return False
    def can_tunnel_east(self):
        if self.east and self.east.east and self.east.vertical_passage():
            return True
        else:
            return False
        
    def horizontal_passage(self):
        return (self.linked(self.east) and self.linked(self.west) and 
                not self.linked(self.north) and not self.linked(self.south))
        
    def vertical_passage(self):
        return ( not self.linked(self.east) and not self.linked(self.west) and 
                self.linked(self.north) and self.linked(self.south))
        
    def link(self, cell, bidir=True):
        if self.north and self.north == cell.south:
            neighbor = self.north
        elif self.south and self.south == cell.north:
            neighbor = self.south
        elif self.west and self.west == cell.east:
            neighbor = self.west
        elif self.east and self.east == cell.west:
            neighbor = self.east
            
        if neighbor:
            self.grid.tunnel_under(neighbor)