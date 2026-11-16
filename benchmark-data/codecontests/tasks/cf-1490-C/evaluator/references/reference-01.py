t = int(input()) 
f = []
for _ in range(t): 
    n = int(input())
    cubes = {}
    for i in range(1,int(n**(1./3.))+8): 
        cubes[i**3] = 1
    for i in range(1,len(cubes)): 
        a = i**3
        b = n - a
        g = cubes.get(b)
        if (g == None): 
            ans = "No"
        else:
            ans = "Yes"
            break
    f.append(ans)
for k in f:
    print(k)