import numpy as np

class Sudoku:
    def __init__(self, size=9, table=[]):
        if size > 9:
            raise "ERROR: Sudoku must be at most 9x9!"
        if len(table) == 0:
            self.table = np.zeros((size, size), dtype=np.int64)
        else:
            self.table = np.array(table)
        self.size = size
    
    """

    Returns TRUE if there is a violation.
    Returns FALSE if there is not a violation

    """
    def check_for_violations(self):
        # Check lines
        for i in range(self.size):
            analysis = self.table[i][self.table[i] != 0]
            if len(np.unique(analysis)) < len(analysis):
                return True

        # Check columns
        for i in range(self.size):
            analysis = self.table.T[i][self.table.T[i] != 0]
            if len(np.unique(analysis)) < len(analysis):
                return True
        
        # Check quadrant
        for i in range(self.size//3):
            for j in range(self.size//3):
                quadrant = self.table[3*i:3*i+3, 3*j:3*j+3].reshape((1, self.size))
                analysis = quadrant[quadrant != 0]
                if len(np.unique(analysis)) < len(analysis):
                    return True
        
        return False
    
    """

    Returns TRUE if all positions have acquired a value.
    Returns FALSE if any position still has no value (represented by 0).
    
    """
    def is_fullfiled(self):
        return not (self.table == 0).any()
    
    """

    Returns TRUE if it is a valid solution
    Returns FALSE if it is not a valid solution

    """
    def is_valid(self):
        return self.is_fullfiled() and (not self.check_for_violations())
    
    def alter_value(self, x, y, value):
        self.table[x][y] = value
    
    def find_empty_coords(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.table[i][j] == 0:
                    return i, j
        return None, None