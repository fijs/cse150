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
    
    #for value in variable.domain
    pass   
