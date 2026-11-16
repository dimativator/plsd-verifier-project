n = int(input())
a = list(map(int,input().split()))
max = a[len(a)-1]
sum = max
for i in range(len(a)-2,-1,-1):
    # print(max)
    if (max<=0):
        break
    if (a[i]>=max):
        # print(a[i])
        max = max-1
        sum += max
    else:
        # print(a[i])
        max = a[i]
        sum += max
print(sum)