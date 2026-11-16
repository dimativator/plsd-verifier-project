n = int(input())
data = input().split()
max = 0
for i in range(n):
    back = max
    if max<int(data[i]):
        max=int(data[i])
    if i==0 and data[i]!="0":
        print(1)
        exit()
    elif int(data[i])>back+1:
        print(i+1)
        exit()
if int(data[i])<=back+1:
    print(-1)
