n = int(input())
m = [[int(i) for i in input().split()] for i in range(n)]

#l = [ sum(m[i]) for i in range(n) ]
#l = l.index(max(l))

print(max([ sum(m[i]) for i in range(n) ]))