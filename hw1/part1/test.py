import skeleton as solution

valid_test_cases = {
    """
    x = 1 + 1;
    y = x + x;
    z = y ^ 2;
    print(z);
    """ : [16],
    
    """
    x = 1 + 2 * 10;
    y = (1+2) * 10;
    print(x);
    print(y);
    """ : [21,30],

    """
    x = 2 - 3 - 4;
    y = 2 - (3 - 4);
    print(x);
    print(y);
    """ : [-5,3],

    # Test - Operator Precedence
    """
    a = 1;
    print(a);
    b = 5 - (a + 2);
    print(b);
    c = 20 / (4 * b);
    print(c);
    d = c ^ 2 ^ 2;
    print(d);
    e = c + b * d ^ 0.25;
    print(e);
    f = 1.5 + (a + b) ^ 2 - e / 2.5 * 1.5;
    print(f);
    """ : [1, 2, 2.5, 39.0625, 7.5, 6],

    # Test - Variable Scope
    """
    a = 1; b = 2;
    print(a);
    print(b);
    {
        print(a);
        { print(b); }
        a = 3;
        { print(a); }
        print(a);
        {
            b = 4;
            print(b);
        }
        print(b);
    }
    print(a);
    print(b);
    """ : [1, 2, 1, 2, 3, 3, 4, 2, 1, 2],

    # Test - Mixed
    """
    printed = 123;
    print(printed);
    a = 3; b = 2; c = 3;
    {
        a = b;
        print(a);
    }
    print(a);
    """ : [123, 2, 3]
}

parsing_error_test_cases = [
    """
    x = 1 ++ 1;
    """,
    
    """
    5 = 1 + 2 * 10;
    """,

    """
    x = 2 - 3 - 4;
    y = 2 - (3 - 4)
    """,

    # Test - Keywords
    """
    print = 1;
    """

    # Test - Parentheses & Braces
    """
    a = (1 + 2;
    """,
    """
    {
        { a = 1;
    }
    """,

    # Test - Unsupported Operators
    """
    a = 2 ** 2;
    """,
    """
    a += 1;
    """
]

symbol_table_error_test_cases = [
    """
    x = 1 + z;    
    """,
    
    """
    {
      x = 12 + 6;
    }
    z = x + x;
    """,

    """
    x = 62 + 78;
    {
       z = x + 1;
       {
         y = z + x;
       }
       w = y;
    }
    """,
    
    # Test - Use before declaration
    """
    a = b;
    """,
    """
    { b = 1; }
    a = b;
    """,
    """
    a = 1;
    c = a + b;
    """,
    """
    {
        {
            {
                {
                    {
                        a = b;
                    }
                }
            }
        }
    }
    """
]


for t in valid_test_cases:
    x = solution.parse_string(t)
    compare = valid_test_cases[t]
    for v in zip(x,compare):
        assert(str(v[0]) == str(v[1]))

for t in parsing_error_test_cases:
    try:
        solution.parse_string(t)
    except solution.ParsingException:
        pass
    else:
        assert(False)

for t in symbol_table_error_test_cases:
    try:
        solution.parse_string(t)
    except solution.SymbolTableException:
        pass
    else:
        assert(False)

