from formula_tree import *
from formula_game_functions_2 import build_tree, find_operator_index, evaluate
def find_num_variables(formula):
    set_of_vars = set()
    for char in formula:
        if(char.isalpha()):
            set_of_vars.add(char)
    result = ""
    for var in set_of_vars:
        result += var
    return result


def find_minterms(formula_tree, var_sequence, var_values):
    """ Given a formula tree and a sequence of variables, return a list
    of minterms for the formula tree, where the lowercase characters
    represent the variable negated and the uppercase characters
    represent the variable as is.
    
    >>> tree = build_tree("(a+b)")
    >>> l = find_minterms(tree, "ab", "")
    >>> l == ['aB', 'Ab', 'AB']
    True
    
    """
    list_of_minterms = []
    if(len(var_values) == len(var_sequence)):
        truth_value = evaluate(formula_tree, var_sequence, var_values)
        if(truth_value == 1):
            minterm = ""
            for i in range(len(var_sequence)):
                if(var_values[i] == "1"):
                    minterm += var_sequence[i].upper()
                else:
                    minterm += var_sequence[i].lower()
            list_of_minterms.append(minterm)
    else:
        list_of_minterms_0 = find_minterms(formula_tree, var_sequence, 
                                           var_values + "0")
        list_of_minterms_1 = find_minterms(formula_tree, var_sequence,
                                           var_values + "1")
        list_of_minterms = list_of_minterms_0 + list_of_minterms_1
    return list_of_minterms