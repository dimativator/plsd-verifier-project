n = int(input())
a1 = [int(s) for s in input().split()]
a2 = [int(s) for s in input().split()]
b = [int(s) for s in input().split()]

sum = 0
for i in range(n-1):
    sum = sum + a2[i]

sum1 = min(sum + b[0], sum - a2[0] + a1[0] + b[1])
sum2 = max(sum + b[0], sum - a2[0] + a1[0] + b[1])

sum = sum - a2[0] + a1[0] + b[1]

for i in range(2, n):
    sum = sum + b[i] - b[i-1] + a1[i-1] - a2[i-1]
    if sum < sum1:
        sum2 = min(sum2,sum1)
        sum1 = sum
    else:
        sum2 = min(sum2, sum)

print(sum1+sum2)
        
