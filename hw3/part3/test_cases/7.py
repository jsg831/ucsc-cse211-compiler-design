for i in range(7,10):
    for j in range(i,100):
        for k in range(0,j):
            for m in range(i,j):
                for q in range(10,100):
                    read_index(k+i+j*q)
                    write_index(m*q+1)
