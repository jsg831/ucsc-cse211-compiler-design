import ply.lex as lex
import ply.yacc as yacc

tokens = ['CHARACTER', 'UNION', 'DOT', 'STAR', 'OPEN_PAREN', 'CLOSE_PAREN', "QUESTION"]

# characters we will support in our regex
t_CHARACTER = '[a-zA-Z0-9]'

# Special characters need to be escaped
t_UNION = '\|'
t_DOT = '\.'
t_STAR = '\*'
t_OPEN_PAREN = '\('
t_CLOSE_PAREN = '\)'
t_QUESTION = '\?'

# Ignore spaces
t_ignore = ' '

# Required in case of a lexing error
def t_error(t):
    print("lexing error!")
    exit(0)

# Build the lexer
lexer = lex.lex()

# The regular expression tree classes. Do not use these functions
class Leaf:
    def __init__(self, character):
        self.char = character

class Op:
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

# Use these functions to build and check your REs instead
def is_epsilon(my_re):
    if isinstance(my_re, Leaf):
        if my_re.char == "":
            return True
    return False

def is_empty(my_re):
    if my_re is None:
        return True
    return False

def mk_union(re1, re2):
    if is_empty(re1):
        return re2
    if is_empty(re2):
        return re1
    if is_epsilon(re1) and is_epsilon(re2):
        return re1
    return Op(re1, re2, "UNION")

def mk_concat(re1, re2):
    if is_empty(re1) or is_empty(re2):
        return None
    if is_epsilon(re1):
        return re2
    if is_epsilon(re2):
        return re1
    return Op(re1, re2, "CONCAT")

def mk_star(re1):
    if is_empty(re1):
        return None
    if is_epsilon(re1):
        return re1
    return Op(re1, None, "STAR")

def mk_epsilon():
    return Leaf("")

def mk_leaf(c):    
    return Leaf(c)

## Nullable definitions starting here:

# Top level Nullable function: this function takes an RE and returns
# the RE for the empty set (None) if the RE matches the empty string
# (epsilon). If the RE matches the empty string, it returns the RE for
# the empty string (epsilon).
def nullable(re):    
    if isinstance(re, Leaf):
        if is_epsilon(re):
            return re
        else:
            return None
        
    if isinstance(re, Op):
        if re.op == "CONCAT":
            return nullable_concat(re)

        if re.op == "UNION":
            return nullable_union(re)

        if re.op == "STAR":
            return mk_epsilon()

# The nullable implementation for an RE node that is a CONCAT operator
def nullable_concat(re):
    nullable_lhs = nullable(re.lhs)
    nullable_rhs = nullable(re.rhs)
    return mk_concat(nullable_lhs, nullable_rhs)

# Homework step 1: implement this function
# The nullable implementation for an RE node that is a UNION operator
def nullable_union(re):
    nullable_lhs = nullable(re.lhs)
    nullable_rhs = nullable(re.rhs)
    return mk_union(nullable_lhs, nullable_rhs)

# Begin Derivative function: This function takes a character (char)
# and an RE (re). It returns the RE that is the derivative of re with
# respect to char.

# More specifically: say the input RE (re) accepts the set of strings S.
# The derivative of re with respect to char is all strings in S that began
# with char, and now have char ommitted. Here are some examples:

# Given a RE (call it re) that matches the language {aaa, abb, ba, bb,
# ""}, the derivative of re with respect to 'a' is {aa, bb}. These are
# the original strings that began with 'a' (namely {aaa, abb}), with
# the first 'a' character removed. Please review the lecture or the
# "Regular-expression derivatives reexamined" for more information

# Top level derivative function:
def derivative_re(char, re):
    if is_empty(re):
        return None
    
    if isinstance(re, Leaf):
        if is_epsilon(re):
            return None
        elif re.char == char:
            return mk_epsilon()
        else:
            return None
        
    if isinstance(re, Op):
        if re.op == "CONCAT":
            return derivative_re_concat(char, re)
        
        if re.op == "UNION":
            return derivative_re_union(char, re)

        if re.op == "STAR":
            return derivative_re_star(char, re)
                    
        assert(False)

# Returns the derivative of a UNION re with respect to char
def derivative_re_union(char, re):
    return mk_union(derivative_re(char, re.lhs), derivative_re(char, re.rhs))

# Homework step 2: Implement this function.
# Returns the derivative of a STAR re with respect to char
def derivative_re_star(char, re):
    # Example: derivative("a", "(a.b.c)*") -> "(b.c).(a.b.c)*"
    return mk_concat(derivative_re(char, re.lhs), re)

# Homework step 3: Implement this function. Recall that the nullable
# function returns an RE that you can use as an argument to build a
# bigger RE.
# Returns the derivative of a CONCAT re with respect to char
def derivative_re_concat(char, re):
    # Case 1: LHS is not nullable ->            derivative of LHS <concat> RHS
    # Case 2: LHS is     nullable -> UNION with derivative of RHS
    return mk_union(
        mk_concat(derivative_re(char, re.lhs), re.rhs),
        mk_concat(nullable(re.lhs), derivative_re(char, re.rhs))
    )

# High-level function to match a string using regular experession
# derivatives:
def parse_re(re, to_match):

    # create the derivative for each character of the string in sequence
    for char in to_match:
        re =  derivative_re(char, re)
        if re is None:
            return False

    # the string matches if and only if the empty string is matched by the derivative RE
    return is_epsilon(nullable(re))

# Parsing the regular expression with Yacc: The reverse precedence
# goes: union, concat, star, parentheses, so they are parsed in this
# order.
def p_re_singleton(p):
    're : concat'
    p[0] = p[1]

def p_re_recusive(p):
    're : concat UNION re'
    p[0] = mk_union(p[1], p[3])

def p_concat_single(p):
    'concat : base'
    p[0] = p[1]

def p_concat_recusive(p):
    'concat : base DOT concat'
    p[0] = mk_concat(p[1], p[3])

def p_base_singleton(p):
    'base : paren'
    p[0] = p[1]

def p_base_star_recursive(p):
    'base : base STAR'
    p[0] = mk_star(p[1])

def p_base_optional_recursive(p):
    'base : base QUESTION'
    # "(<re>)? := (<re> | <empty_string>)"
    p[0] = mk_union(p[1], mk_epsilon())

def p_paren_singleton(p):
    'paren : symbol'
    p[0] = p[1]

def p_paren_recursive(p):
    'paren : OPEN_PAREN re CLOSE_PAREN'
    p[0] = p[2]

def p_symbol(p):
    'symbol : CHARACTER'
    p[0] = mk_leaf(p[1])

def p_error(p):
    print("parsing error!")
    exit(0)

parser = yacc.yacc()

# Keep this function exactly how it is for grading to use with the tester scripts.
def match_regex(reg_ex, string):
    d_re = parser.parse(reg_ex)
    return parse_re(d_re, string)

# Use this conditional to test your script locally
if __name__ == "__main__":
    d_re = parser.parse("(h.i)? | c.s.e*.2.1.1")

    # should pass
    print(parse_re(d_re, "") == True)
    print(parse_re(d_re, "hi") == True)    
    print(parse_re(d_re, "cse211") == True)
    print(parse_re(d_re, "cs211") == True)
    print(parse_re(d_re, "cseee211") == True)

    # should fail
    print(parse_re(d_re, "hihi") == False)
    print(parse_re(d_re, "hhh") == False)
    print(parse_re(d_re, "cseee21") == False)
    print(parse_re(d_re, "211") == False)
