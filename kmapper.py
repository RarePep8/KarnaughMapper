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

def simplify_minterms(list_of_minterms):
    done_simplifying = False
    simplified_minterms = set()
    while(not done_simplifying and len(list_of_minterms) > 1):
        simplified_indices = set()
        done_simplifying = True
        for i in range(len(list_of_minterms)):
            for j in range(i+1, len(list_of_minterms)):
                if(len(list_of_minterms[i]) == len(list_of_minterms[j])):
                    (can_simplify, new_minterm) = diff_minterms(list_of_minterms[i], list_of_minterms[j])
                    if(can_simplify):
                        print("hi")
                        simplified_indices.add(i)
                        simplified_indices.add(j)
                        done_simplifying = False
                        simplified_minterms.add(new_minterm)
            if(i not in simplified_indices):
                simplified_minterms.add(list_of_minterms[i])
        if(len(list_of_minterms)-1 not in simplified_indices):
            simplified_minterms.add(list_of_minterms[-1])
        
        list_of_minterms = list(simplified_minterms)
        simplified_minterms = set()
    return list_of_minterms

def diff_minterms(m1, m2):
    num_diff = 0
    new_minterm = ""
    for i in range(len(m1)):
        if(m1[i] == "?" and m2[i] == "?"):
            new_minterm += "?"
        elif(m1[i] == "?" or m2[i] == "?"):
            new_minterm += "?"
            num_diff += 1
        elif(m1[i] != m2[i]):
            num_diff += 1
            new_minterm += "?"
        else:
            new_minterm += m1[i]
    if(num_diff != 1):
        can_simplify = False
    else:
        can_simplify = True
    print(new_minterm)
    return (can_simplify, new_minterm)

def format_minterms(simplified_minterms):
    new_minterms = set()
    for minterm in simplified_minterms:
        new_minterm = ""
        for char in minterm:
            if(char != "?"):
                new_minterm += char
        if(new_minterm != ""):
            new_minterms.add(new_minterm)
    return new_minterms


#tree = build_tree("((((((((a*-b)*(-c*-d))*((-a*b)*(-c*-d)))*((a*b)*(-c*-d)))*((a*-b)*(c*-d)))*((a*b)*(c*-d)))*((a*b)*(-c*d)))*((a*-b)*(c*d)))")
tree = build_tree("(((a+b)*b)+a)")
l = find_minterms(tree, "ab", "")
print(l)
l = simplify_minterms(l)
print(l)
l = format_minterms(l)
print(l)