# skeleton file for UCSC CSE211 Homework 2: part 1

from pycfg.pycfg import PyCFG, CFGNode, slurp 
import argparse 
import re

# Acks: I used
# https://www.geeksforgeeks.org/draw-control-flow-graph-using-pycfg-python/
# to get started with PyCFG. 

# Given a node, returns the instruction as a string
# instructions are of the form:
def get_node_instruction(n):
    return n.attr["label"]

# Given a CFG and a node, return a list of successor nodes
def get_node_successors(CFG, n):
    return CFG.successors(n)

# given a node instruction string (e.g. from get_node_instruction),
# returns the name of the variable that is read (if any)
def reads_var(i):

    # matches "if" instructions of the form: <label>: if: <var>
    # returns <var> because it is a read variable
    if "if" in i:
        return re.match("\d+:\s*if:\s*(\S+)",i)[1]

    # matches "while" instructions of the form: <label>: while: <var>
    # returns <var> because it is a read variable
    if "while" in i:
        return re.match("\d+:\s*while:\s*(\S+)",i)[1]

    # inputs don't read any variable
    if "input" in i:
        return None

    # special nodes (start and stop) do not read anything
    if "start" in i or "stop" in i:
        return None

    # otherwise the instruction is an assignment of the form:
    # <label>: <var> = <var>
    # Returns the rhs variable
    assert("=" in i)
    return re.match("\d+:\s*(\S+)\s*=\s*(\S+)",i)[2]

# given a node instruction string (e.g. from get_node_instruction),
# returns the name of the variable that is written (if any)
def writes_var(i):

    # if statements in this subset don't write to any variables
    if "if" in i:
        return None

    # while loops in this subset don't write to any variables
    if "while" in i:
        return None

    # inputs write to the lhs variable
    if "input" in i:
        return re.match("\d+:\s*(\S+)\s*=\s*input\(\)",i)[1]

    # special nodes (start and stop) do not write to a variable
    if "start" in i or "stop" in i:
        return None

    # otherwise the instruction is an assignment of the form:
    # <label>: <var> = <var>
    # Returns the lhs variable
    assert("=" in i)
    return re.match("\d+:\s*(\S+)\s*=\s*(\S+)",i)[1]

# use PyCFG to get a CFG of the python input file.  Graph is returned
# as a PyGraphviz graph.  Don't worry too much about this function. It
# just uses the PyCFG API
def get_graph(input_file):
    cfg = PyCFG()
    cfg.gen_cfg(slurp(input_file).strip())
    arcs = []
    return CFGNode.to_graph(arcs)

# get the domain of all the variables. This is needed for the set
# compliment of VarKill in the iterative algorithm to compute LiveOut
def compute_VarDomain(CFG):

    # start with an empty set
    VarDomain = set({})

    # for each node in the CFG
    for n in CFG.nodes():

        # get the variables that are read from
        var1 = reads_var(get_node_instruction(n))

        # get the variables that are written to
        var2 = writes_var(get_node_instruction(n))

        # only add the variables if they are not None
        if var1 is not None:
            VarDomain = VarDomain.union(set([var1]))
        if var2 is not None:
            VarDomain = VarDomain.union(set([var2]))

    # return the final set
    return VarDomain

# get the UEVar set:
# hint: iterate over all the nodes and record only some of the variables
# used. Use reads_var and/or writes_var function to get variables
def compute_UEVar(CFG):
    UEVar = {}

    # Homework: implement this function.
    for n in CFG.nodes():
        UEVar[n] = reads_var(get_node_instruction(n))
        
    return UEVar

# get the VarKill set:
# hint: iterate over all the nodes and record only some of the variables
# used. Use reads_var and/or writes_var function to get variables
def compute_VarKill(CFG):
    VarKill = {}

    # Homework: implement this function.
    for n in CFG.nodes():
        VarKill[n] = writes_var(get_node_instruction(n))

    return VarKill

# iteratively compute LiveOut

# hint: this will be a fixed point iteration. It should look
# a lot like figure 8.14b in the EAC book.

# You can use get_node_successors(CFG, n) to get a list of n's
# successor nodes.
def compute_LiveOut(CFG, UEVar, VarKill, VarDomain):

    LiveOut = {}

    # Homework: implement this function.

    # Types of order:
    #   "default"  : node number 0,1,2,3,...
    #   "rpo"      : reverse post-order on CFG (essentially BFS on CFG)
    #   "rpo_rcfg" : reverse post-order on reverse CFG (essentially BFS on reverse CFG)

    order = 'rpo_rcfg'

    if order == 'default':
        nodes = CFG.nodes()
    elif order == 'rpo':
        nodes = []
        visited = set({})
        queue = [CFG.get_node(0)]
        while len(queue):
            n = queue.pop()
            nodes.append(n)
            visited.add(n)
            for m in get_node_successors(CFG, n):
                if m not in visited:
                    queue.append(m)
    elif order == 'rpo_rcfg':
        nodes = []
        visited = set({})
        queue = [CFG.get_node(len(CFG.nodes())-1)]
        while len(queue):
            n = queue.pop()
            nodes.append(n)
            visited.add(n)
            for m in CFG.predecessors(n):
                if m not in visited:
                    queue.append(m)

    for n in nodes:
        LiveOut[n] = set({})

    changed = True
    num_iter = 0
    while changed:
        num_iter += 1
        changed = False
        for n in nodes:
            new_LiveOut = set({})
            for m in get_node_successors(CFG, n):
                if UEVar[m]:
                    new_LiveOut.add(UEVar[m])
                VarKillBar = VarDomain - set({VarKill[m]})
                new_LiveOut = new_LiveOut.union(LiveOut[m].intersection(VarKillBar))
            if new_LiveOut != LiveOut[n]:
                LiveOut[n] = new_LiveOut
                changed = True
    print("#Iter = {}".format(num_iter))

    return LiveOut

# NOTE: TEST RESULTS ON TRAVERSAL ORDER
# 
#              ___________________________ #ITERATIONS
#             |       |        |     
#             V       V        V     
# +------+---------+-----+----------+
# | TEST | default | rpo | rpo_rcfg |
# +------+---------+-----+----------+
# |   0  |    2    |  2  |     2    |
# |   1  |    5    |  2  |     2    |
# |   2  |    5    |  2  |     2    |
# |   3  |    6    |  2  |     3    |
# |   4  |    7    |  2  |     3    |
# |   5  |    6    |  2  |     3    |
# |   6  |    8    |  2  |     3    |
# |   7  |    8    |  2  |     3    |
# +------+---------+-----+----------+
# 
# NOTE: OBSERVATIONS
#
#    1. LiveOut propagates from the child to the parent, so it's better to from the bottom of the graph.
#    2. The default order is not very representative because it can be any order except for the first node and the last node.
#    3. The "rpo" or reverse post-order on CFG is the worst case because it follows the opposite direction of LiveOut propagation.
#    4. The "rpo_rcfg" is the best order because LiveOut flows from the last node to the first.
#    5. Ideally on a DAG the optimal #iter should be 2, but there are cases where 3 iterations are necessary.
#       I think the extra iterations are due to loops, where LiveOut needs to be passed at least twice to reach stable states.

# The uninitialized variables are the LiveOut variables from the start
# node. It is fine if your implementation needs to change this
# function. It simply needs to return a set of uninitialized variables
def get_uninitialized_variables_from_LiveOut(CFG, LiveOut):
    return LiveOut[CFG.get_node(0)]

# The testing function. Keep the signature of this function the
# same as it will be used for grading. I highly recommend you keep the
# function exactly the same and simply implement the constituent
# functions.
def find_undefined_variables(input_python_file):

    # Convert the python file into a CFG
    CFG = get_graph(input_python_file)

    # Get the variable domain (used to compute the VarKill set
    # compliment in the iterative algorithm)
    VarDomain = compute_VarDomain(CFG)

    # Get UEVar
    UEVar    = compute_UEVar(CFG)

    # Get VarKill
    VarKill  = compute_VarKill(CFG)

    # Get LiveOut
    LiveOut = compute_LiveOut(CFG, UEVar, VarKill, VarDomain)

    # Return a set of unintialized variables
    return get_uninitialized_variables_from_LiveOut(CFG, LiveOut)

# if you run this file, you can give it one of the python test cases
# in the test_cases/ directory.
# see solutions.py for what to expect for each test case.
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()   
    parser.add_argument('pythonfile', help ='The python file to be analyzed') 
    args = parser.parse_args()
    print(find_undefined_variables(args.pythonfile))
