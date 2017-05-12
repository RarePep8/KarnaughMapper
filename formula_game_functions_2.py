"""
# Copyright Nick Cheng, Alex Wong 2017
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment

# Add your functions here.


def build_tree(formula):
    ''' (str) -> FormulaTree or NoneType

    Given a string representation of a formula, return a tree representation
    of it with FormulaTree objects, if the formula is invalid then return
    None instead

    >>> build_tree("") == None
    True
    >>> build_tree("(-x)") == None
    True
    >>> build_tree("x+y") == None
    True
    >>> build_tree("x*y") == None
    True
    >>> build_tree("x-y") == None
    True
    >>> build_tree("(x+2)") == None
    True
    >>> build_tree("X") == None
    True
    >>> build_tree("(x+y+z)") == None
    True
    >>> build_tree("(x+(y)+z)") == None
    True
    >>> build_tree("((x)(x+y))") == None
    True
    >>> build_tree("(((x+)(x+y)))") == None
    True
    >>> build_tree("x") == Leaf("x")
    True
    >>> build_tree("(n+m)") == OrTree(Leaf("n"), Leaf("m"))
    True
    >>> build_tree("(c*v)") == AndTree(Leaf("c"), Leaf("v"))
    True
    >>> build_tree("-x") == NotTree(Leaf("x"))
    True
    >>> build_tree("-((x+y)*(a*-b))") == NotTree(AndTree(OrTree(Leaf("x"),\
Leaf("y")), AndTree(Leaf("a"), NotTree(Leaf("b")))))
    True
    '''
    # If formula is 1 character, create a leaf from it if it's a valid
    # variable name, otherwise return None
    if(len(formula) == 1):
        if(formula.isalpha() and formula.islower()):
            result = Leaf(formula)
        else:
            result = None
    # If the formula is an empty string, it is invalid therefore return None
    elif(len(formula) == 0):
        result = None
    else:
        # If the first character is -, then first build the smaller subtree
        # and create a NotTree for the subtree if the subtree is valid
        if(formula[0] == "-"):
            child1 = build_tree(formula[1:])
            if(child1 is None):
                result = None
            else:
                result = NotTree(child1)
        # if the first and last characters are brackets then
        elif(formula[0] == "(" and formula[-1] == ")" and
             formula.count("(") == formula.count(")")):
            # find the operator that accompanies the bracket pair
            index = find_operator_index(formula)
            # if the operator is found, build the smaller subtree called
            # child1 from the left, build the smaller subtree called child2
            # from the right, and from those create an AndTree or
            # OrTree based on the operator.
            if(index != -1):
                child1 = build_tree(formula[1:index])
                child2 = build_tree(formula[index+1:-1])
                if(child1 is None or child2 is None):
                    result = None
                else:
                    if(formula[index] == "*"):
                        result = AndTree(child1, child2)
                    else:
                        result = OrTree(child1, child2)
            # if index is -1, it means there is no corresponding operator,
            # which means the formula is invalid
            else:
                result = None
        # If the leading character is neither a single variable, "-",
        # nor "(", then the formula is invalid
        else:
            result = None
    # Return the resulting root of the FormulaTree
    return result


def find_operator_index(formula):
    ''' (str) -> int

    Given a string representation of a formula, return the index of the
    operator ("+" or "*") at the first depth/level of the formula. If there
    are none, then return -1.

    >>> find_operator_index("x")
    -1
    >>> find_operator_index("(x+y)")
    2
    >>> find_operator_index("(x*y)")
    2
    >>> find_operator_index("-((x*y)+(a*b))")
    7
    >>> find_operator_index("(xy)")
    -1
    >>> find_operator_index("+)(x+y")
    -1
    >>> find_operator_index("+")
    -1
    '''
    bracket_groups = 0
    index = -1
    # Increase and decrease bracket_groups to show the current depth
    # If "+" or "*" is found at the lowest depth, return its index,
    # otherwise return -1
    for i in range(len(formula)):
        if((formula[i] == "+" or formula[i] == "*") and bracket_groups == 1):
            index = i
        elif(formula[i] == "("):
            bracket_groups += 1
        elif(formula[i] == ")"):
            bracket_groups -= 1
    return index


def evaluate(root, variables, values):
    ''' (FormulaTree, str, str) -> int

    Given a formula tree, a sequence of variables, and a sequence of values
    that corresponds to the variables, evaluate and return an int of
    truth value of the formula tree where 1 is True and 0 is False

    REQ: len(variables) == len(values)

    >>> t = build_tree('x')
    >>> evaluate(t, 'x', '1')
    1

    >>> t = build_tree('-y')
    >>> evaluate(t, 'y', '1')
    0

    >>> t = build_tree('(x+y)')
    >>> evaluate(t, 'yx', '10')
    1

    >>> t = build_tree('(x*y)')
    >>> evaluate(t, 'xy', '10')
    0

    >>> t = build_tree('((x+-x)*(y+-y))')
    >>> evaluate(t, 'xy', '00')
    1

    >>> t = build_tree('((x*-x)+(y*-y))')
    >>> evaluate(t, 'xy', '11')
    0

    '''
    # If the current root is a leaf of a variable, then return the value
    # of the variable from the given sequence of variables and values
    if(root.symbol.isalpha()):
        index = variables.index(root.symbol)
        truth_value = int(values[index])
    else:
        # Obtain the truth value of the smaller subtree
        value1 = evaluate(root.children[0], variables, values)
        # If the current root is a NotTree, then invert the truth value
        if(root.symbol == "-"):
            truth_value = 1-value1
        else:
            # Obtain the truth value of the second smaller subtree
            value2 = evaluate(root.children[1], variables, values)
            # If the current root is an OrTree, return the bigger truth value
            # of the two subtrees
            if(root.symbol == "+"):
                truth_value = max(value1, value2)
            # If the current root is an AndTree, return the smaller truth
            # value of the two subtrees
            else:
                truth_value = min(value1, value2)
    return truth_value


