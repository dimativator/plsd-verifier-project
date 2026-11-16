n = int(input())
l = [int(x) for x in input().split()]

while len(l) > 1:
    
    if len([i for i in range(len(l)-1) if abs(l[i] - l[i+1]) > 1 ])>0:
        print ('NO')
        exit(0)
    
    l.remove(max(l))

print('YES')
        