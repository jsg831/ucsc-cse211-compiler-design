from skeleton import match_regex

tests = [("z", "z", True),
         ("z", "y", False),
         ("z.z", "zz", True),
         ("z.z", "yz", False),
         ("z|y", "z", True),
         ("z|y", "y", True),
         ("z|y", "w", False),
         ("z.z|y", "zz", True),
         ("z.z|y", "y", True),
         ("z.z|y", "z", False),
         ("e*", "", True),
         ("e*", "eeeeee", True),
         ("e*", "eeezeee", False),
         ("(z|y*).z", "yyyz", True),
         ("(z|y*).z", "zyyy", False),
         ("c.s.e.2.1.1*", "cse21", True),
         ("c.s.e.2.1.1*", "cse2111", True),
         ("c.s.e.2.1.1*", "cs211", False),
         ("u.c.s.c*|s.l.u.g.s|c.s*.e", "csssse", True),
         ("u.c.s.c*|s.l.u.g.s|c.s*.e", "slug", False),
         ("u.c.s.c*|s.l.u.g.s|c.s*.e", "slugs", True),
         ("u.c.s.c*|s.l.u.g.s|c.s*.e", "ucs", True),
         ("u.c.s.c*|s.l.u.g.s|c.s*.e", "ucslugs", False)]

failed = 0
total = len(tests)
for t in tests:
    result = match_regex(t[0], t[1])
    if result != t[2]:
        failed += 1
        print("--")
        print("failed: matching string " + t[1] + " to regex " + t[0])
        print("expected " + str(t[2]))
        print("got " + str(result))
        print("--")
        #exit(0)

print("total tests: " + str(total))
print("passed: " + str(total - failed))
print("failed: " + str(failed))
