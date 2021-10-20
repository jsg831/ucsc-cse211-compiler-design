import test_cases
import skeleton as candidate

test_blocks = eval("[" + ",".join(sorted(["test_cases."+x for x in dir(test_cases) if "test_block" in x])) + "]")
test_results = eval("[" + ",".join(sorted(["test_cases."+x for x in dir(test_cases) if "test_result" in x])) + "]")

passed_1 = 0
failed_1 = 0

passed_2 = 0
failed_2 = 0

passed_3 = 0
failed_3 = 0

passed_4 = 0
failed_4 = 0

total_1 = 0
total_2 = 0
total_3 = 0
total_4 = 0

for idx in range(len(test_blocks)):
    bb = test_blocks[idx]
    result = test_results[idx]
    res = candidate.check_replaced_instructions(bb)

    total_1 += res[1]
    total_2 += res[3]
    total_3 += res[5]
    total_4 += res[7]
    
    
    some_failed = False

    if result[0] != res[1]:
        failed_1 += 1
        some_failed = True
    else:
        passed_1 += 1

    if result[1] != res[3]:
        failed_2 += 1
        some_failed = True
    else:
        passed_2 += 1

    if result[2] != res[5]:
        failed_3 += 1
        some_failed = True
    else:
        passed_3 += 1

    if result[3] != res[7]:
        failed_4 += 1
        some_failed = True
    else:
        passed_4 += 1


    
    if some_failed:
        print("----------------------")
        print("failed on test case: " + str(idx))
        print(bb.pprint())
        print("expected number of removed instructions for each part: " + str(result))
        print("found: " + str([res[1], res[3], res[5], res[7]]))
        print("----------------------")

print("---------")
print("part 1:")
print("passed: " + str(passed_1))
print("failed: " + str(failed_1))
print("total removed operations: " + str(total_1))

print("---------")
print("part 2:")
print("passed: " + str(passed_2))
print("failed: " + str(failed_2))
print("total removed operations: " + str(total_2))

print("---------")
print("part 3:")
print("passed: " + str(passed_3))
print("failed: " + str(failed_3))
print("total removed operations: " + str(total_3))

print("---------")
print("part 4:")
print("passed: " + str(passed_4))
print("failed: " + str(failed_4))
print("total removed operations: " + str(total_4))
