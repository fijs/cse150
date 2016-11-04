# -*- coding: utf-8 -*-

from collections import deque


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise.
    """

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    # TODO implement this

    # print queue_arcs
    # list of variables
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

def check_value_consistency(constraints, val1, var2):
    for val2 in var2.domain:
        if check_constraints(constraints, val1, val2):
            return True

    return False

def check_constraints(constraints, val1, val2):
    for constraint in constraints:
        if not constraint.is_satisfied(val1, val2):
            return False

    return True

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

def revise(csp, xi, xj):
    # You may additionally want to implement the 'revise' method.
    pass