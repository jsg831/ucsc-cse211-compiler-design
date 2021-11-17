import os
import argparse

# Top of C++ file with includes and namespaces
top_source_string = """
#include <iostream>
#include <assert.h>
#include <chrono>
using namespace std;
using namespace std::chrono;

typedef double reduce_type;

"""

# The reference loop simply adds together all elements in the array
def reference_reduction_source():

    # function header
    function = "void reference_reduction(reduce_type *b, int size) {"

    # loop header
    loop = "  for (int i = 1; i < size; i++) {"

    #simple reduction equation
    eq = "    b[0] += b[i];"

    # closing braces
    loop_close = "  }"
    function_close = "}"

    # joining together all parts
    return "\n".join([function, loop, eq, loop_close, function_close])

# Your homework will largely take place here. Create a loop that
# is semantically equivalent to the reference loop. That is, it computes
# a[0] = a[0] + a[1] + a[2] + a[3] + a[4] ... + a[size]
#
# where size is passed in by the main source string.
#
# You should unroll by a factor of "partitions". This is done logically
# by splitting a into N partitions (where N == partitions). You will compute
# N reductions, one computation for each partition per loop iteration.
#
# You will need a cleanup loop after the main loop to combine
# the values in each partition.
#
# You can assume the size and the number of partitions will be
# a power of 2, which should make the partitioning logic simpler.
#
# You can gain confidence in your solution by running the code
# with several power-of-2 unroll factors, e.g. 2,4,8,16. You
# should pass the assertion in the code.
#
# You can assume partition is less than size.
def homework_reduction_source(partitions):
    # header
    function = "void homework_reduction(reduce_type *a, int size) {"
    
    # NOTE: Assume we can modified the value of any a[i] in place
    #       (equivalent implementation should use extra space for >1 partitions)
    
    # Process `partitions` elements per loop iteration
    loop = "  for (int i = {0}; i < size; i += {0}) {{".format(partitions)
    chain = []
    # Temporary sum of partition `i` is stored in a[`i`]
    for i in range(0,partitions):
        chain.append("    a[{0}] += a[i+{0}];".format(i))
    loop_close = "  }"
    # Clean-up loop: sum of partition sums
    second_loop = "  for (int i = 1; i < {0}; i++) a[0] += a[i];".format(partitions)
    function_body = "\n".join([loop, "\n".join(chain), loop_close, second_loop])

    # closing brace
    function_close = "}"
    return "\n".join([function, function_body,function_close])

# String for the main function, including timings and
# reference checks.
# Modified to 64M elements because of memory limit on my laptop
main_source_string = """
#define SIZE (1024*1024*64)


int main() {
  reduce_type *a;
  a = (reduce_type *) malloc(SIZE * sizeof(reduce_type));

  reduce_type *b;
  b = (reduce_type *) malloc(SIZE * sizeof(reduce_type));

  for (int i = 0; i < SIZE; i++) {
    a[i] = 1;
    b[i] = 1;
  }

  auto new_start = high_resolution_clock::now();
  homework_reduction(a,SIZE);
  auto new_stop = high_resolution_clock::now();
  auto new_duration = duration_cast<nanoseconds>(new_stop - new_start);
  double new_seconds = new_duration.count()/1000000000.0;

  auto ref_start = high_resolution_clock::now();
  reference_reduction(b,SIZE);
  auto ref_stop = high_resolution_clock::now();
  auto ref_duration = duration_cast<nanoseconds>(ref_stop - ref_start);
  double ref_seconds = ref_duration.count()/1000000000.0;

  cout << "new loop time: " << new_seconds << endl; 
  cout << "reference loop time: " << ref_seconds << endl; 
  cout << "speedup: " << ref_seconds / new_seconds << endl << endl;

  if (a[0] != b[0]) cout << a[0] << " != " << b[0] << endl;

  return 0;
}
"""

# Create the program source code
def pp_program(partitions):

    # Your function is called here
    homework_string = homework_reduction_source(partitions)

    print(homework_string)
    # View your homework source string here for debugging
    return "\n".join([top_source_string, reference_reduction_source(), homework_string, main_source_string])

# Write a string to a file (helper function)
def write_str_to_file(st, fname):
    f = open(fname, 'w')
    f.write(st)
    f.close()

# Compile the program. Don't change the options here for the official
# assignment report. Feel free to change them for your own curiosity.
# Some notes:
#
# I am using a recent version of C++ to use the chrono library.
#
# I am disabling the compiler's loop unrolling so we can ensure the
# reference loop and the homework loops are not unrolled "behind our backs"
#
# I am using the highest optimization level (-O3) to illustrate that
# the compiler is not even brave enough to perform this optimization!
def compile_program():
    cmd = "clang++ -std=c++17 -fno-unroll-loops -O3 -o homework homework.cpp"
    print("running: " + cmd)
    assert(os.system(cmd) == 0)

# Run the program
def run_program():
    cmd = "./homework"
    print("running: " + cmd)
    print("")
    assert(os.system(cmd) == 0)

# This is the top level program function. Generate the C++ program,
# compile it, and run it.
def generate_and_run(partitions):
    print("")
    print("----------")
    print("generating and running for:")
    print("partitions = " + str(partitions))
    print("-----")
    print("")

    # get the C++ source
    program_str = pp_program(partitions)

    # write it to a file (homework.cpp)
    write_str_to_file(program_str, "homework.cpp")

    # compile the program
    compile_program()

    # run the program
    run_program()

# gets one command line arg unroll factor (UF)                                               
def main():
    parser = argparse.ArgumentParser(description='Part 2 of Homework 1: exploiting ILP by unrolling reduction loop iterations.')
    parser.add_argument('unroll_factor', metavar='UF', type=int,
                   help='how many loop iterations to unroll')
    args = parser.parse_args()
    UF = args.unroll_factor
    generate_and_run(UF)

if __name__ == "__main__":
    main()
