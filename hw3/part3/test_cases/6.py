for i in range(7,10):
    for j in range(i,100):
        for k in range(0,j):
            read_index(k*5)
            write_index(i*j*k)
