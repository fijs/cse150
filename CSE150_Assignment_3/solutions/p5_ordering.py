# -*- coding: utf-8 -*-
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
    unassigned_vars = (variable for variable in csp.variables if not variable.is_assigned())
    min_var_list = []
    min_domain = sys.maxint

    for var in unassigned_vars:
        domain_size = len(var.domain)

        if domain_size == min_domain:
            min_var_list.append(var)
        elif domain_size < min_domain:
            min_var_list = [var]
            min_domain = domain_size

    if len(min_var_list) == 1:
        return min_var_list[0]

    max_constraints = -sys.maxint - 1
    all_constraints = csp.constraints
    max_constraint_var = None

    for var in min_var_list:
        constraint_list = [constraint for constraint in all_constraints[var]
                           if not constraint.var2.is_assigned()]
        num_constraints = len(constraint_list)
        if num_constraints > max_constraints:
            max_constraints = num_constraints
            max_constraint_var = var

    return max_constraint_var


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
