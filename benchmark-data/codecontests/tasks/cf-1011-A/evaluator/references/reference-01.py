n,k = list(map(int,input().split()))

data = sorted(list(input()))

data = list(map(lambda x:ord(x)-ord('a')+1,data))

result = 0
used = 0
idx =0
prev = -2


# print(data)

for d in data:
    if d > prev+1:
        result+= d
        prev = d
        used += 1


    if used == k:
        break

if used < k:
    print(-1)
else:
    print(result)

