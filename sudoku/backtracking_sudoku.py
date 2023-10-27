from sudoku import Sudoku
import numpy as np

class BacktrackAgent:
    def __init__(self, env : Sudoku):
        self.env = env
    
    def act(self, domain, allSolutions=False):
        if self.env.is_fullfiled():
            if not allSolutions:
                return self.env.table
            print(self.env.table)
        else:
            for value in domain:
                tmp = self.env.table.copy() # Old solution so we can backtrack
                i, j = self.env.find_empty_coords() # Next place to place a value
                self.env.alter_value(i, j, value)

                if not self.env.check_for_violations():
                    result = self.act(domain, allSolutions)
                    if not allSolutions:
                        if (result != None).all():
                            return result
                
                self.env.table = tmp # Backtracking
            return np.array([None])

if __name__ == "__main__":
    env = Sudoku()
    ag = BacktrackAgent(env)
    solution = ag.act([1,2,3,4,5,6,7,8,9], allSolutions=False)
    print(solution)
        