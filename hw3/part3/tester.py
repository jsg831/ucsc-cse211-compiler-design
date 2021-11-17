from skeleton import analyze_file

tests = {"0.py" : False,
         "1.py" : True,
         "2.py" : False,
         "3.py" : True,
         "4.py" : False,
         "5.py" : True,
         "6.py" : False,
         "7.py" : False
}

passed = 0
failed = 0
for t in tests:
    result = tests[t]
    test_file = "test_cases/" + t
    print("running: " + test_file)
    print("")
    res = analyze_file(test_file)
    if res != result:
        print("failed test: " + t)
        failed += 1
    else:
        passed += 1

print("passed: " + str(passed))
print("failed: " + str(failed))
    
