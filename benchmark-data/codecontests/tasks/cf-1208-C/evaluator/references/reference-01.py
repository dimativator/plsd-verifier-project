n = int(input())
for i in range(n):
    printlist = []
    m=i//4
    k=i%4
    for j in range(n):
        printlist.append(str(4*n*m+4*j+k))
    print(' '.join(printlist))
