# skeleton file for UCSC CSE211 Homework 2: part 1

# Variable class: contains a name and an optional number
class Variable:
    def __init__(self, name, number=None):
        self.name = name
        self.number = number

    # Getting the name and number
    def get_name(self):
        return self.name

    def get_number(self):
        return self.number

    # Use this to get a pretty printed string of the Variable
    def pprint(self):
        if self.number is None:
            return self.name
        else:
            return self.name + str(self.number)

    # used for auto test generation. Not needed for the assignment.
    def pprint_code(self):
        return "Variable('" + self.name + "')"


# Class for an assignment instruction. It simply takes a lhs and rhs
# variable: the instruction is of the form: lhs = rhs;
class AssignmentInstr:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    # used for auto test generation. Not needed for the assignment
    def pprint(self):
        return self.lhs.pprint() + " = " + self.rhs.pprint()

# Class for an arithmetic instruction. It takes a lhs (Variable), op1,
# and op2 (Variable) and an op ('+', '-', '*', '/') The form of the
# instruction is: lhs = op1 op op2
class ArithmeticInstr:
    def __init__(self, lhs, op1, op, op2):
        self.lhs = lhs
        self.op1 = op1
        self.op  = op
        self.op2 = op2

    # return a nicely formated string of the arithmetic operation
    def pprint(self):
        return self.lhs.pprint() + " = " + self.op1.pprint() + " " + self.op + " " + self.op2.pprint()

    # used for auto test generation. Not needed for the assignment.
    def pprint_code(self):
        return "ArithmeticInstr(" + ",".join([self.lhs.pprint_code(), self.op1.pprint_code(), "'" + self.op + "'", self.op2.pprint_code()]) + ")"

# A class for a basic block, essentially a list of operations
class BasicBlock:
    def __init__(self, l):
        self.instrs = l

    # add an instruction to the end of the basic block
    def add_instruction(self, i):
        self.instrs.append(i)

    # returns a pretty printed string of the basic block
    def pprint(self):
        pp_list = [i.pprint() for i in self.instrs]
        return "\n".join(pp_list)

    # get the list of instructions, assignment or arithmetic operations
    def instruction_list(self):
        return self.instrs

    # used for auto test generation. Not needed for the assignment.
    def print_test_case(self, test_id, removed1, removed2, removed3, removed4):
        ret = "test_block" + str(test_id) + " = BasicBlock(["
        instr_list = [i.pprint_code() for i in self.instrs]
        ret += ",\n".join(instr_list) + "])\n"
        ret += "test_result" + str(test_id) + " = [" + str(removed1) + ", " + str(removed2) + ", " + str(removed3) + ", " + str(removed4)  + "]\n"
        return ret

# Given a variable name (v), a map from variables to their most recent
# numbering (v_map), and the current value: determine if a new value
# is needed. If so, update the hashtable, and increment the
# value. Otherwise just return the value in the hash table.
def get_var_value(value, v_map, v):
    if v in v_map:
        return v_map[v],value
    else:
        v_map[v] = value
        return value, value + 1

# Given a basic block of unnumbered variables, return a basic block
# with numbered variables
def do_numbering(input_block):
    value = 0
    var_to_value = {}

    # New block to return. Its empty and we'll add instructions to it.
    return_block = BasicBlock([])

    # iterate through the basic block instructions
    for instr in input_block.instruction_list():
        # Assume only arithmetic operations
        # Assume that the basic block is not numbered
        op1 = instr.op1
        op2 = instr.op2
        result = instr.lhs
        op = instr.op

        # get the numbering for op1 and create a new variable with op1
        # name and the numbering
        op1_numbering, value = get_var_value(value, var_to_value, op1.get_name())
        op1_var = Variable(op1.get_name(), op1_numbering)

        # same for op2
        op2_numbering, value = get_var_value(value, var_to_value, op2.get_name())
        op2_var = Variable(op2.get_name(), op2_numbering)

        # Assigments always update the numbering
        result_numbering = value
        var_to_value[result.get_name()] = result_numbering
        value += 1
        
        result_var = Variable(result.get_name(), result_numbering)
        
        # Add new numbered instruction
        new_instr = ArithmeticInstr(result_var, op1_var, op, op2_var)

        # Add it to the new block
        return_block.add_instruction(new_instr)
        
    return return_block

# Homework part1: Implement this function, which takes in a basic
# block with numbered variables. It is your job to find redundent
# arithmetic instructions and replace them with assignment
# instructions

# For part1, you can not assume any commutative operations. You can
# assume numbered variables are new variables. That is, a0 is distinct
# from a1

# you should iterate over instructions. You can assume that all
# variables are numbered and that all instructions are arithmetic
# instructions.

# It should return the new block, along with an integer indicating how
# many arithmetic instructions were replaced with assignment
# instructions

# I have provided the start of an implementation for you
def replace_redundant_part1(input_block):

    # block to return
    return_block = BasicBlock([])

    # increment every time an arithmetic instruction is replaced
    replaced_instructions = 0
    for instr in input_block.instruction_list():

        # You can assume only arithmetic operations        
        lhs    = instr.lhs # a variable on the lhs of the assignment
        op1    = instr.op1 # the first operand 
        op     = instr.op  # the operator; one of ('+', '-', '*', '/')
        op2    = instr.op2 # the seecond operand

        # You can access names and numbers of the variables with, e.g.:
        # op1.get_name()
        # op1.get_number()

        # Determine if the instruction can be replaced, if not you
        # should simply add the original instruction to the return_block

        # you can create an assignment instruction with the constructor:        # new_instr = AssignmentInstr(lhs_variable, rhs_variable)       
        return_block.add_instruction(instr)
        
    return return_block, replaced_instructions

# Homework part2: Implement this function, which takes in a basic
# block with numbered variables. It is your job to find redundent
# arithmetic instructions and replace them with assignment
# instructions

# For part2, you need to take into account commutative operations (+,
# *). Like in part1, you can assume numbered variables are new
# variables. That is, a0 is different from a1

# Your solution should be similar to part1, only with a check for
# commutative instructions

# I have provided the start of an implementation for you
def replace_redundant_part2(input_block):

    # block to return
    return_block = BasicBlock([])

    # increment every time an arithmetic instruction is replaced
    replaced_instructions = 0
    for instr in input_block.instruction_list():

        # You can assume only arithmetic operations        
        lhs    = instr.lhs # a variable on the lhs of the assignment
        op1    = instr.op1 # the first operand 
        op     = instr.op  # the operator; one of ('+', '-', '*', '/')
        op2    = instr.op2 # the seecond operand

        # You can access names and numbers of the variables with, e.g.:
        # op1.get_name()
        # op1.get_number()

        # Determine if the instruction can be replaced, if not you
        # should simply add the original instruction to the return_block

        # you can create an assignment instruction with the constructor:        # new_instr = AssignmentInstr(lhs_variable, rhs_variable)       

        return_block.add_instruction(instr)
        
    return return_block, replaced_instructions

# Homework part3: Implement this function, which takes in a basic
# block with numbered variables. It is your job to find redundent
# arithmetic instructions and replace them with assignment
# instructions

# For part3, you should assume (+,*) are commutative (like in part2).
# The difference here is that you CANNOT assume numbered variables are
# distinct. That is, a0 is NOT different than a1. This means that your
# replacement check needs to determine if the variable has not been
# assigned a new value more recently.

# For example, consider the program:
# a = b + c
# a = x + y
# z = b + c

# You cannot replace z = b + c because 'a' no longer contains 'b + c',
# it was overwitten.

# Your solution should be similar to part2, with the additional check
# for the most recent variable version.
def replace_redundant_part3(input_block):

    # block to return
    return_block = BasicBlock([])

    # increment every time an arithmetic instruction is replaced
    replaced_instructions = 0
    for instr in input_block.instruction_list():

        # You can assume only arithmetic operations        
        lhs    = instr.lhs # a variable on the lhs of the assignment
        op1    = instr.op1 # the first operand 
        op     = instr.op  # the operator; one of ('+', '-', '*', '/')
        op2    = instr.op2 # the seecond operand

        # You can access names and numbers of the variables with, e.g.:
        # op1.get_name()
        # op1.get_number()

        # Determine if the instruction can be replaced, if not you
        # should simply add the original instruction to the return_block

        # you can create an assignment instruction with the constructor:        # new_instr = AssignmentInstr(lhs_variable, rhs_variable)       

        return_block.add_instruction(instr)
        
    return return_block, replaced_instructions

# Homework part4: Implement this function, which takes in a basic
# block with numbered variables. It is your job to find redundent
# arithmetic instructions and replace them with assignment
# instructions

# For part4, you must also consider commutative operations.  like in
# part 3, numbers do not make variables distinct. a0 is NOT different
# than a1. The difference in part 4 is that you must track a set of
# candidate replacements.

# For example, consider a slightly different program from part 3:
# a = b + c
# q = b + c
# a = x + y
# z = b + c

# You cannot replace 'z = b + c' with 'z = a' because 'a' no longer
# contains 'b + c', it was overwitten. BUT you can replace it with
# 'q', because 'q' also contains 'b+c' and it was NOT overwritten.
def replace_redundant_part4(input_block):

    # block to return
    return_block = BasicBlock([])

    # increment every time an arithmetic instruction is replaced
    replaced_instructions = 0
    for instr in input_block.instruction_list():

        # You can assume only arithmetic operations        
        lhs    = instr.lhs # a variable on the lhs of the assignment
        op1    = instr.op1 # the first operand 
        op     = instr.op  # the operator; one of ('+', '-', '*', '/')
        op2    = instr.op2 # the seecond operand

        # You can access names and numbers of the variables with, e.g.:
        # op1.get_name()
        # op1.get_number()

        # Determine if the instruction can be replaced, if not you
        # should simply add the original instruction to the return_block

        # you can create an assignment instruction with the constructor:        # new_instr = AssignmentInstr(lhs_variable, rhs_variable)       
        return_block.add_instruction(instr)
        
    return return_block, replaced_instructions

# This is required for grading. It runs all 4 parts and returns how
# many operations were replaced.
def check_replaced_instructions(b):

    # get a numbered block
    numbered_block = do_numbering(b)

    # the function will return the block (resN_b) and the
    # count of replaced instructions (resN_c)
    res1_b, res1_c = replace_redundant_part1(numbered_block)
    res2_b, res2_c = replace_redundant_part2(numbered_block)
    res3_b, res3_c = replace_redundant_part3(numbered_block)
    res4_b, res4_c = replace_redundant_part4(numbered_block)
    
    return [res1_b, res1_c, res2_b, res2_c, res3_b, res3_c, res4_b, res4_c]

# Some simple test cases to get you started
PLUS = "+"
MINUS = "-"
vA = Variable("a")
vB = Variable("b")
vC = Variable("c")
vD = Variable("d")
vE = Variable("e")
vF = Variable("f")

block1 = BasicBlock(
          [
          ArithmeticInstr(vA, vB, PLUS, vC),
          ArithmeticInstr(vB, vA, MINUS, vD),
          ArithmeticInstr(vC, vB, PLUS, vC),
          ArithmeticInstr(vD, vA, MINUS, vD)
          ]
          )

block2 = BasicBlock([ArithmeticInstr(vA, vB, PLUS, vC),
          ArithmeticInstr(vB, vA, PLUS, vD),
          ArithmeticInstr(vC, vB, PLUS, vC),
          ArithmeticInstr(vD, vD, PLUS, vA)])

block3 = BasicBlock([ArithmeticInstr(vA, vB, PLUS, vC),
          ArithmeticInstr(vB, vA, MINUS, vD),
          ArithmeticInstr(vC, vB, PLUS, vC),
          ArithmeticInstr(vD, vD, MINUS, vA)])

block4 = BasicBlock([ArithmeticInstr(vA, vB, PLUS, vC),
          ArithmeticInstr(vD, vB, PLUS, vC),
          ArithmeticInstr(vD, vB, PLUS, vC),
          ArithmeticInstr(vC, vB, PLUS, vC),])

block5 = BasicBlock([ArithmeticInstr(vB, vB, PLUS, vB),
          ArithmeticInstr(vB, vB, PLUS, vB),
          ArithmeticInstr(vB, vB, PLUS, vB),
          ArithmeticInstr(vB, vB, PLUS, vB),])

block6 = BasicBlock([ArithmeticInstr(vA, vC, PLUS, vD),
          ArithmeticInstr(vB, vC, PLUS, vD),
          ArithmeticInstr(vA, vF, PLUS, vF),
          ArithmeticInstr(vE, vC, PLUS, vD),])

# Some local checks to help you debug.
def check_block(block, p1, p2, p3, p4):
    res = check_replaced_instructions(block)
    assert(res[1] == p1)
    assert(res[3] == p2)
    assert(res[5] == p3)
    assert(res[7] == p4)

if __name__ == "__main__":
    check_block(block1, 1, 1, 1, 1)
    check_block(block2, 0, 1, 1, 1)
    check_block(block3, 0, 0, 0, 0)
    check_block(block4, 3, 3, 3, 3)
    check_block(block5, 0, 0, 0, 0)
    check_block(block6, 2, 2, 1, 2)
