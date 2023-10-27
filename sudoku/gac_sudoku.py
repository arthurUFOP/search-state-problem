import numpy as np

# Generalized Arc Consistency (GAC) algorithm for Sudoku

# REMEMBER: All restrictions in Sudoku are of the type A1 != A2

# i = 0, 3, 6
# j = 0, 3, 6
def get_quadrant_vector(matrix, i, j):
   return matrix[i:i+3, j:j+3].reshape(9,)
    
def scope(constraint):
    return set([constraint[0], constraint[1]])

"""
General Gac can be found at https://artint.info/3e/html/ArtInt3e.Ch4.S3.html

V -> Variables
dom -> Variables domain
cs -> Restrictions
to_do -> Restrictions to analysis (initially all of them)

"""
# dom is dict of sets
#cs -> set ([(1, 2), (4, 5)])
def GAC(V, dom : dict, cs, to_do : set): 
    while len(to_do) > 0: 
        var, constraint = to_do.pop() # int, (int, int)
        constraint_scope = scope(constraint) - set([var])
        constraint_var = constraint_scope.pop() # For sudoku, it will allways be one var

        new_domain = set()
        for x in dom[var]:
            for y in dom[constraint_var]:
                if x != y:
                    new_domain.add(y)

        if new_domain != dom[constraint_var]:
            for z in V:
                for c_line in cs:
                    if scope(c_line) != scope(constraint) and {z, var}.issubset(scope(c_line)) and z!=var:
                        to_do.add((z, (z, var)))

            dom[constraint_var] = new_domain
        
    return dom

if __name__ == "__main__":
    variables = [x for x in range(81)]
    domain = {x : set(i+1 for i in range(9)) for x in variables}
    # Lines => set(range(x+1, (x//9)*9+9))
    # Columns => set(range(x+9, 81, 9))

    # Quadrant constraint => 
    helper = np.arange(0, 81).reshape((9, 9))
    quadrants = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            quadrants.append(get_quadrant_vector(helper, i, j))
    
    quadrant_constraints = set()
    for quadrant in quadrants:
        for i in range(9):
            for j in range(i+1, 9):
                quadrant_constraints.add((quadrant[i], quadrant[j]))

    constraints = set((x, x_line) for x in variables for x_line in set(range(x+1, (x//9)*9+9)).union(set(range(x+9, 81, 9)))).union(quadrant_constraints)
    
    # Constraints, in this case, MUST BE simetric
    sim_cons = set()
    for x, y in constraints:
        sim_cons.add((y, x))
    constraints = constraints.union(sim_cons)

    to_do = set((x, c) for x in variables for c in constraints if x==c[0])

    # ---------------------------------------------------------------------------------
    #                                 TEST CASES

    # Test case 1
    # Now Line 1, Quadrant 1 and Column 1 must change their domains!
    domain[0] = {1}

    # Test case 2
    # Now Line 1 and 3, Column 1 and 2 and quadrant 1 must change their domains!
    #domain[0] = {1}
    #domain[19] = {3}

    # Test case 3
    # Now Line 1 and 3 and 9, Column 1 and 2 and 9 and quadrant 1 and 9 must change their domains!
    #domain[0] = {1}
    #domain[19] = {3}
    #domain[80] = {9}

    # Test case 4
    # Now Line 1 and 3 and 9 and 5, Column 1 and 2 and 9 and 5 and quadrant 1 and 9 and 5 must change their domains!
    #domain[0] = {1}
    #domain[19] = {3}
    #domain[80] = {9}
    #domain[40] = {5}

    # Test case 5 - Constraint violation
    # All sets should have their domains changed to {}
    #domain[0] = {1}
    #domain[1] = {1} # This causes the constraint violation 
    #domain[19] = {3}
    #domain[80] = {9}
    #domain[40] = {5}


    # ---------------------------------------------------------------------------------

    n_domain = GAC(variables, domain.copy(), constraints, to_do)
    print("DOMAINS THAT WERE AFFECTED:")
    for n_key in n_domain.keys():
        if domain[n_key] != n_domain[n_key]:
            print("------------------------------\n")
            print(f"Key {n_key} = Position ({n_key//9 + 1}, {n_key - (n_key//9)*9 + 1})")
            print(f"Comparison on key {n_key}: ")
            print("Old Domain: ", domain[n_key])
            print("New Domain: ", n_domain[n_key])
            print("")

    