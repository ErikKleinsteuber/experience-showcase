"""
The exercise is to create a (almost) general constraint satisfaction problem
solver. You will have to use the CSP data structure from csp.py. Read it for
reference!

"""
import numpy as np
import csp
from data import create_map_csp

def _select_unassigned(possibleVars):

    #print "searching for new variable"
    #print possibleVars

    for x in possibleVars:
        if x.get_value() == None:
            var = x
    return var

def _select_mrv(possibleVars,assignment,csp):
    
    a = []
    for x in possibleVars:
        if x.get_value() == None:
            y = 0
            for value in x.domain:
                if _check_consistency(x,value,assignment,csp):
                    y += 1
            if y > 0:
                a.append((x,y))

    a.sort(key=lambda x:x[1])
    return a[0][0]

def _select_mrv_tie(possibleVars,assignment,csp):
    
    a = []
    for x in possibleVars:
        if x.get_value() == None:
            y = 0
            for value in x.domain:
                if _check_consistency(x,value,assignment,csp):
                    y += 1
            if y > 0:
                a.append((x,y))

    a.sort(key=lambda x:x[1])
    ti = a[0][1]
    for x in a[:]:
        if x[1] != ti:
            a.remove(x)
    
    b=[]
    for x in a:
        consts = set(csp.get_constraints_for_variable(x[0]))
        b.append((x[0],len(consts)))
    
    b.sort(key=lambda x:x[1], reverse=True)
    return b[0][0]


#CHECKS-CONTRAINT-CONSISTENCY-OF-ONE-SPECIFIC-VALUE
def _check_consistency(var, value, assignment, csp):
    consts = set(csp.get_constraints_for_variable(var))
    for x in set(consts):
        if not (x.var1 in assignment) and not (x.var2 in assignment):
            consts.remove(x)

    var.set_value(value)
    b = all( (x.consistent() for x in consts) )
    var.set_value(None)
    return b

#RECURSIVE-BACKTRACKING
def _rec(assignment, csp):
    #flag = True
    #for v in csp.variables:
    #    if v.get_value() == None:
    #        flag = False
    #if flag:
    #    return assignment
    
    #print "Solution is: "
    #print csp.complete()
    if csp.complete() == True:              #edit 14.01. morgens, ersetzt die Abfrage oben
        return assignment
    
    #SELECT-UNASSIGNED-VARIABLE
    var = _select_unassigned(csp.variables) # hier geschieht der Fehler
                                            # Sudoku ist zwar vollkommen belegt, aber immernoch false
                                            # wie kann das sein, wenn wir nur Sudoku-logisch richtige
                                            # Variablen in assignment abspeichern?
    
    #for each <value> in ORDERED-DOMAIN-VALUES[] DO:
    for value in var.domain:
        #check if the value satisfies all constraints in the actual scenario
        if _check_consistency(var, value, assignment, csp):
            
            #add [var = value] to assignment
            #(sets in csp as well as assignment)
            var.set_value(value)
            assignment.append(var)
            
            #propagate result
            result = _rec(assignment, csp)
            
            #if the recursion does not end in a failure
            if result != None:
                #propagate result
                return result
            
            var.set_value(None) #edit 14.01. morgens
            assignment.remove(var)
    return None
    
#BACKTRACKING-SEARCH
def backtracking(csp, ac_3=False):
    """
    Implement the basic backtracking algorithm to solve a CSP.

    Optional: if ac_3 == True use the AC-3 algorithm for constraint
              propagation. Important: if ac_3 == false don't use
              AC-3!
    :param csp: A csp.ConstrainedSatisfactionProblem object
                representing the CSP to solve
    :return: A csp.ConstrainedSatisfactionProblem, where all Variables
             are set and csp.complete() returns True. (I.e. the solved
             CSP)
    """
    
    #print "CSP.VARIABLES in the beginning: "
    #print csp.variables
    
    
    #print "Starting Backtracking"
    _rec([], csp)
    
    #print "CSP.VARIABLES: "
    #print csp.variables
    
    return csp
    
    pass

#REC2 ANOTHER VERSION OF rec
def _rec2(assignment, csp):
    if csp.complete() == True:              #edit 14.01. morgens, ersetzt die Abfrage oben
        return assignment
    
    #SELECT-UNASSIGNED-VARIABLE
    var = _select_mrv(csp.variables, assignment, csp)
    
    #for each <value> in ORDERED-DOMAIN-VALUES[] DO:
    for value in var.domain:
        #check if the value satisfies all constraints in the actual scenario
        if _check_consistency(var, value, assignment, csp):
            #sets in csp as well as assignment
            var.set_value(value)
            assignment.append(var)
            
            #propagate result
            result = _rec(assignment, csp)
            
            #if the recursion does not end in a failure
            if result != None:
                #propagate result
                return result
            
            #else, ... recursion failed
            assignment.remove(var)
    return None
    
def minimum_remaining_values(csp, ac_3=False):
    """
    Implement the basic backtracking algorithm to solve a CSP with
    minimum remaining values heuristic and no tie-breaker. Thus the
    first of all best solution is taken.

    Optional: if ac_3 == True use the AC-3 algorithm for constraint
              propagation. Important: if ac_3 == false don't use
              AC-3!
    :param csp: A csp.ConstrainedSatisfactionProblem object
                representing the CSP to solve
    :return: A tuple of 1) a csp.ConstrainedSatisfactionProblem, where
             all Variables are set and csp.complete() returns True. (I.e.
             the solved CSP) and 2) a list of all variables in the order
             they have been assigned.
    """
    assigns = _rec2([], csp)
    return csp,assigns

#RECURSIVE-BACKTRACKING
def _rec3(assignment, csp):
    if csp.complete() == True:              #edit 14.01. morgens, ersetzt die Abfrage oben
        return assignment
    
    #SELECT-UNASSIGNED-VARIABLE
    var = _select_mrv_tie(csp.variables, assignment, csp)
    
    #for each <value> in ORDERED-DOMAIN-VALUES[] DO:
    for value in var.domain:
        #check if the value satisfies all constraints in the actual scenario
        if _check_consistency(var, value, assignment, csp):
            #sets in csp as well as assignment
            var.set_value(value)
            assignment.append(var)
            #propagate result
            result = _rec(assignment, csp)
            
            #if the recursion does not end in a failure
            if result != None:
                #propagate result
                return result
            
            #else, ... recursion failed
            assignment.remove(var)
    return None
def minimum_remaining_values_with_degree(csp, ac_3=False):
    """
    Implement the basic backtracking algorithm to solve a CSP with
    minimum remaining values heuristic and the degree heuristic as
    tie-breaker.

    Optional: if ac_3 == True use the AC-3 algorithm for constraint
              propagation. Important: if ac_3 == false don't use
              AC-3!
    :param csp: A csp.ConstrainedSatisfactionProblem object
                representing the CSP to solve
    :return: A tuple of 1) a csp.ConstrainedSatisfactionProblem, where
             all Variables are set and csp.complete() returns True. (I.e.
             the solved CSP) and 2) a list of all variables in the order
             they have been assigned.
    """
    assigns = _rec3([], csp)
    return csp,assigns


def create_sudoku_csp(sudoku):
    """
    Creates a csp.ConstrainedSatisfactionProblem from a numpy array
    `sudoku` which has shape (9, 9). Each entry of the sudoku is either
    0, which means it is not set yet or in [1, ..., 9], which means
    it is already assigned a number.

    The CSP should contain all constraints necessary to solve the sudoku.
    I.e. no two numbers in a row must be equal, no two numbers in a column
    must be equal and no two numbers in one of the 9 3x3 blocks must be
    equal. All numbers in the array must be already set.

    :param sudoku: A numpy array representing a unsolved sudoku
    :return: A csp.ConstrainedSatisfactionProblem which can be used
             to solve the sudoku
    """
    X = 9
    Y = 9
    variables = [[] for y in range(X)]
    constraints = set()
    
    
    #create vars
    for x in range(X):
        for y in range(Y):
            newName = str(x*X+y)
            if sudoku[x,y] != 0:
                variables[x].append(csp.Variable(newName, [], sudoku[x,y])) #empty domain cause number given
            else:
                variables[x].append(csp.Variable(newName, [1,2,3,4,5,6,7,8,9], None)) #no number given, so no value and full domain is specifiyed
    
    #spalten
    #print "befor spalte",len(constraints)
    for c in range(X):
        column = set()
        for y in range(Y):
            column.add(variables[c][y])
            
        for e1 in column:
            for e2 in column:
                if e1 != e2:
                    constraints.add(csp.UnequalConstraint(e1,e2))
    #print "after spalte",len(constraints)
    #zeilen
    for r in range(Y):
        row = set()
        for x in range(X):
            row.add(variables[x][r])
        for e1 in row:
            for e2 in row:
                if e1 != e2:
                    constraints.add(csp.UnequalConstraint(e1,e2))
    #print "after zeile",len(constraints)
    for ux in range(3):
        for uy in range(3):
            unit = set()
            for x in range(3):
                for y in range(3):
                    unit.add(variables[ux*3+x][uy*3+y])
            for e1 in unit:
                for e2 in unit:
                    if e1 != e2:
                        constraints.add(csp.UnequalConstraint(e1,e2))
    #print "var_len:",len(variables)
    #print "con_len:",len(constraints)
    
    var = set()
    for x in range(X):
        for y in range(Y):
            var.add(variables[x][y])
    return csp.ConstrainedSatisfactionProblem(var, constraints)


def sudoku_csp_to_array(csp):
    """
    Takes a sudoku CSP from `create_sudoku_csp()` as you implemented
    it and returns a numpy array s with `s.shape == (9, 9)` (i.e. a
    9x9 matrix) representing the sudoku.

    :param csp: The CSP created with `create_sudoku_csp()`
    :return: A numpy array with shape (9, 9)
    """
    sudoku = np.zeros((9,9))
    for v in csp.variables:
        name = int(v.name)
        x = name/9
        y = name%9
        sudoku[x,y] = v.get_value()
    return sudoku

def read_sudokus():
    """
    Reads the sudokus in the sudoku.txt and saves them as numpy arrays.
    :return: A list of np.arrays containing the sudokus
    """
    with open("sudoku.txt", "r") as f:
        lines = f.readlines()
    sudoku_strs = []
    for line in lines:
        if line[0] == 'G':
            sudoku_strs.append("")
        else:
            sudoku_strs[-1] += line.replace("", " ")[1:]
    sudokus = []
    for sudoku_str in sudoku_strs:
        sudokus.append(np.fromstring(sudoku_str, sep=' ',
                                     dtype=np.int).reshape((9, 9)))
    return sudokus


def main():
    """
    A main function. This might be useful for developing, if you don't
    want to run all tests all the time. Just write here what ever you
    want to develop your code. If you use pycharm you can run the unittests
    also by right-clicking them and then e.g. "Run 'Unittest test_sudoku_1'".
    """

    # first lets test with a already created csp:
    csp = create_map_csp()
    solution = backtracking(csp)
    print(solution)

    # and now with our own generated sudoku CSP
    sudokus = read_sudokus()
    csp = create_sudoku_csp(sudokus[2])

    solution = backtracking(csp)
    print(solution)

if __name__ == '__main__':
    main()
