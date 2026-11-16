n,v=[int(x) for x in input().split()]
if n<=v+1:
    print(n-1)
else:
    print(v+(n-v-1)*(n-v-2)//2+(n-v-1)*2)
