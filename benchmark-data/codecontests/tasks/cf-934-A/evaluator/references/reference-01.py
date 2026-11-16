n, m = [int(x) for x in input().split()]
lstT = [int(x) for x in input().split()]
lstB = [int(x) for x in input().split()]
z=-9999999999999999999999999999
T=0
B=0
for i in range(n):
        for j in range(m):
                if z<lstT[i]*lstB[j]:
                        T=i
                        B=j
                        z=lstT[i]*lstB[j]
lol = -99999999999999999999
for i in range(n):
        for j in range(m):
                if T!=i:
                        lol = max(lol, lstT[i]*lstB[j])
print(lol)
