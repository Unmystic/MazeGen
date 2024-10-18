import random
from PIL import Image

class Mask(object):
    
    def from_txt(file):
        
        with open(file,"r") as f:
            lines = f.readlines()
            lines = [line.rstrip('\n') for line in lines]
            rows = len(lines)
            cols = len(lines[0])
            
            mask = Mask(rows,cols)
            for i in range(rows):
                for j in range(cols):
                    if lines[i][j] == "X":
                        mask.set_switch(i,j,False)
        return mask
    
    def from_png(file):
        
        img = Image.open(file)
        img = img.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
        img = img.transpose(method=Image.Transpose.ROTATE_90)
        mask = Mask(img.height, img.width)
        for i in range(img.height):
            for j in range(img.width):
                if img.getpixel((i, j)) == (0,0,0,255):
                    mask.set_switch(i,j,False)
        return mask
        

    
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.bits = [[True for j in range(self.columns)] for i in range(self.rows)]
        
    def check_switch(self, row, column):
        if 0 <= row < self.rows and 0<= column < self.columns:
            return self.bits[row][column]
        else:
            return False
    
    def set_switch(self, row,column, is_on:bool):
        if (0 <= row < self.rows and 0<= column < self.columns) and isinstance(is_on, bool):
            self.bits[row][column] = is_on
        elif not isinstance(is_on, bool):
            raise TypeError("Parameter is_on must be a boolean")
        else:
            raise IndexError("Check yo rows and cols")
        
    def count(self):
        count = 0      
        for i in range(self.rows):
            for j in range(self.columns):
                if self.bits[i][j]:
                    count += 1
        return count
    
    def random_location(self):
        
        while True:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.columns - 1)
            
            if self.bits[row][col]:
                return [row,col]
    

                
    
if __name__ == "__main__":
    mask = Mask(3,4)   
    print(mask.bits)
    print(mask.check_switch(1,3))
    mask.set_switch(1,3, False)
    print(mask.check_switch(1,3))

    print(mask.count())
    print(mask.random_location())
    
    
    