# -*- coding: utf-8 -*-
import sys

import sys

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

def check_constraints(constraints, val1, val2):
    for constraint in constraints:
        if not constraint.is_satisfied(val1, val2):
            return False

    return True
