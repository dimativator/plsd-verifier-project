n = int(input())
for _ in range(n):
    a,b = map(int,input().split())
    if a!=b:
        print ('Happy Alex')
        exit()
print ('Poor Alex')