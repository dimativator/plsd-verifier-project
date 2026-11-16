n, m = map(int, input().split())
a = list( map(int, input().split()) )
b = list( map(int, input().split()) )
i, j, counter = 0, 0, 0
while( i < int(n) and j < int(m) ):
    if( a[i] <= b[j] ):
        i += 1
        j += 1
        counter += 1
    else:
        i += 1
print(counter)            