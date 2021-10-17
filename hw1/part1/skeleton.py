import ply.lex as lex

class SymbolTableException(Exception):
    pass

class ParsingException(Exception):
    pass

# Implement this class, i.e. provide some class members and implement
# the functions.
class SymbolTable:
    """
    Implemented as an array of dictionaries
    """

    def __init__(self):
        # "_st" is the internal data structure for the array of dictionaries
        self._st = [{}]
    
    def insert(self, name, value):
        # New variables belong to the top dictionary
        #print("Assign {} = {}".format(name, value))
        self._st[-1][name] = value

    def lookup(self, name):
        # Search variable name from the top dictionary to the bottom dictionary
        # (Closest scope first)
        for i in range(len(self._st)):
            value = self._st[-1-i].get(name)
            if value is not None:
                return value
        #print("Variable '{}' is not defined".format(name))
        raise SymbolTableException
    
    def push_scope(self):
        # Push an empty dictionary
        self._st.append({})

    def pop_scope(self):
        # Pop the top dictionary
        self._st.pop()

# I have provided you with the token rule to get ids and to get PRINT
# you must provide all other tokens
reserved = {
   'print' : 'PRINT'
}

tokens = ["ID", "NUM", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "EQUAL", "PLUS", "MINUS", "MULT", "DIV", "CARROT", "SEMI"] + list(reserved.values())

# Numbers must start and end with non-zero digits
# Valid   : "1.01", "123", "1012.2"
# Invalid : "1.", "2.0", "012", "012.1"
t_NUM    = r"([1-9][0-9]*|0)(\.([0-9]*[1-9]))?"

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_EQUAL  = r"\="
t_PLUS   = r"\+"
t_MINUS  = r"\-"
t_MULT   = r"\*"
t_DIV    = r"\/"
t_CARROT = r"\^"
t_SEMI   = r";"

# Ignore whitespaces
t_ignore = " \t"

def t_ID(t):
    "[a-zA-Z]+"
    t.type = reserved.get(t.value, 'ID')
    return t

# I have implemented the error function and newline rule for you
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    print("line number: %d" % t.lexer.lineno)
    raise ParsingException()

def t_newline(t):
    "\\n"
    t.lexer.lineno += 1

lexer = lex.lex()

import ply.yacc as yacc

# Global variables I suggest you use (although you are not required)
to_print = []
ST = SymbolTable()

# I have implemented the parsing error function for you
def p_error(p):
    if p is not None:
        print("Syntax error in input on line: %d" % p.lineno)
    else:
        print("Syntax error in input")
    raise ParsingException()

# You must implement all the production rules. Please review slides
# from Oct. 4 if you need a reference.

# Empty (for clarity)
def p_empty(p):
    """
    empty :
    """

# Top
# - Accept 0 or more statements
def p_stmt_list(p):
    """
    stmt_list : stmt stmt_list
              | empty
    """

# Statements
# - 3 types of statements
def p_stmt(p):
    """
    stmt : assignment_stmt
         | print_stmt
         | scope_stmt
    """

# Statement - Assignment
def p_assignment_stmt(p):
    """
    assignment_stmt : ID EQUAL expr SEMI 
    """
    ST.insert(p[1], p[3])

# Statement - Printing
def p_print_stmt(p):
    """
    print_stmt : PRINT LPAREN ID RPAREN SEMI
    """
    val = ST.lookup(p[3]);
    # Check if val can be represented as an integer (no trailing zero)
    if float(val).is_integer():
        to_print.append(int(val))
    else:
        to_print.append(val)

# Statement - Scope
# - Push one scope into the symbol table after entering the inner scope
# - Pop one scope from the symbol table after exiting the inner scope
def p_scope_stmt(p):
    """
    scope_stmt : LBRACE f_lbrace stmt_list RBRACE f_rbrace
    """

def p_f_lbrace(p):
    """
    f_lbrace : empty
    """
    ST.push_scope()

def p_f_rbrace(p):
    """
    f_rbrace : empty
    """
    ST.pop_scope()

# Expressions
# /=======================================\
# | PRECEDENCE | OPERATOR | ASSOCIATIVITY |
# |=======================================|
# |    Low     |   +, -   |     left      |
# |     |      |----------|---------------|
# |     |      |   *, /   |     left      |
# |     |      |----------|---------------|
# |     |      |    ^     |     right     |
# |     V      |----------|---------------|
# |    High    | ( expr ) |       -       |
# \---------------------------------------/

# Notes:   Recursion on which side = Associativity

def p_expr(p):
    """
    expr : expr PLUS  subexpr
         | expr MINUS subexpr
    """
    if p[2] == "+":
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] - p[3]

def p_expr_subexpr(p):
    """
    expr : subexpr
    """
    p[0] = p[1]

def p_subexpr(p):
    """
    subexpr : subexpr MULT powexpr
            | subexpr DIV  powexpr
    """
    if p[2] == "*":
        p[0] = p[1] * p[3]
    else:
        p[0] = p[1] / p[3]

def p_subexpr_powexpr(p):
    """
    subexpr : powexpr
    """
    p[0] = p[1]

def p_powexpr(p):
    """
    powexpr : factor CARROT powexpr
    """
    p[0] = p[1] ** p[3]

def p_powexpr_factor(p):
    """
    powexpr : factor
    """
    p[0] = p[1]

def p_factor_expr(p):
    """
    factor : LPAREN expr RPAREN
    """
    p[0] = p[2]

def p_factor_num(p):
    """
    factor : NUM
    """
    # Store the value as float or int
    if '.' in p[1]:
        p[0] = float(p[1])
    else:
        p[0] = int(p[1])

def p_factor_id(p):
    """
    factor : ID
    """
    p[0] = ST.lookup(p[1])

# Specify top production rule = "stmt_list"
parser = yacc.yacc(debug=True, start="stmt_list")

def parse_string(s):
    global to_print
    global ST
    ST = SymbolTable()
    to_print = []
    parser.parse(s)
    return to_print

# Program
# Example on how to test locally in this file:

'''
parser.parse("""
x = 5 + 4 * 5;
i = 1 + 1 * 0;
print(i);
{
  l = 5 ^ x;
{
    k = 5 + 7;
}
}
q = x / i;
print(q);
""")

for p in to_print:
    print(p)
'''
