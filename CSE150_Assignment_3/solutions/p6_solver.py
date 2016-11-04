# -*- coding: utf-8 -*-

from collections import deque
import sys


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None


def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns True; otherwise, it returns False.
    """
    if is_complete(csp):
        return True
    else:
        var = select_unassigned_variable(csp)
        for value in order_domain_values(csp,var):
            csp.variables.begin_transaction()
            if is_consistent(csp,var,value):
                var.assign(value)
                if inference(csp, var):
                    if backtrack(csp):
                        return True
            csp.variables.rollback()
        return False

def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise.  Note that this method does not
    return any additional variable assignments (for simplicity)."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    # TODO copy from p4
    all_constraints = csp.constraints

    while queue_arcs:
        var1, var2 = queue_arcs.pop()
        curr_constraints = all_constraints[var1, var2]
        inconsistent = []
        for val1 in var1.domain:
            if not check_value_consistency(curr_constraints, val1, var2):
                inconsistent.append(val1)

        if inconsistent:
            var1.domain = [ val for val in var1.domain if val not in inconsistent ]
            if not var1.domain:
                return False
            incoming_arcs = [ (constraint._flip().var1, constraint._flip().var2) for constraint in all_constraints[var1]
                              if constraint not in all_constraints[var1, var2]]
            for arc in incoming_arcs:
                queue_arcs.append(arc)

    return True


### from p1
def is_complete(csp):
    """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""

    # Hint: The list of all variables for the CSP can be obtained by csp.variables.
    # Also, if the variable is assigned, variable.is assigned() will be True.
    # (Note that this can happen either by explicit assignment using variable.assign(value),
    # or when the domain of the variable has been reduced to a single value.)
    for var in csp.variables:
        if not var.is_assigned():
            return False

    return True

### from p2
def is_consistent(csp, variable, value):
    """Returns True when the variable assignment to value is consistent, i.e. it does not violate any of the constraints
    associated with the given variable for the variables that have values assigned.

    For example, if the current variable is X and its neighbors are Y and Z (there are constraints (X,Y) and (X,Z)
    in csp.constraints), and the current assignment as Y=y, we want to check if the value x we want to assign to X
    violates the constraint c(x,y).  This method does not check c(x,Z), because Z is not yet assigned."""

    # TODO implement this
    constraints = csp.constraints
    for var in csp.variables:
        if var == variable:
            continue

        if var.is_assigned():
            for constraint in constraints[var, variable]:
                if not constraint.is_satisfied(var.value, value):
                    return False

    return True


### from p4
def check_constraints(constraints, val1, val2):
    for constraint in constraints:
        if not constraint.is_satisfied(val1, val2):
            return False

    return True

def check_value_consistency(constraints, val1, var2):
    for val2 in var2.domain:
        if check_constraints(constraints, val1, val2):
            return True

    return False

### from p5
def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """

    # TODO implement this
    mrv = sys.maxint
    var = None
    for variable in csp.variables:
       if not variable.is_assigned():
          if len(variable.domain) < mrv:
              var = variable
              mrv = len(variable.domain)
          if len(variable.domain) == mrv:
              constraint_variable = [constraint for constraint in csp.constraints[variable] if
      not constraint.var2.is_assigned()]
              constraint_var = [constraint for constraint in csp.constraints[var] if not
      constraint.var2.is_assigned()]
              if len(constraint_variable) > len(constraint_var):
                 var = variable

    return var


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """

    # TODO implement this
    all_constraints = csp.constraints
    curr_constraints = csp.constraints[variable]

    constraint_list = []
    for val in variable.domain:
        num_mismatch = 0
        for constraint in curr_constraints:
            var2 = constraint.var2
            num_mismatch += count_value_mismatch(all_constraints[variable, var2], val, var2)
        constraint_list.append((val, num_mismatch))

    sorted_list = sorted(constraint_list, key=lambda tup: tup[1])
    result = [tup[0] for tup in sorted_list]

    return result


def count_value_mismatch(constraints, val1, var2):
    mismatch = 0
    for val2 in var2.domain:
        if not check_constraints(constraints, val1, val2):
            mismatch += 1

    return mismatch


