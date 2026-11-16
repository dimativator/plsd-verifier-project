NumOfSocks = int(input())
Socks = [int(x) for x in input().split()]
OnTable, maxSocks, tmpMaxSocks = [0] * (NumOfSocks+1), 0, 0
for i in Socks:
    if not OnTable[i]: 
        OnTable[i] = 1
        tmpMaxSocks += 1
    else:
        OnTable[i] = 0
        tmpMaxSocks -= 1
    if tmpMaxSocks > maxSocks: maxSocks = tmpMaxSocks
print(maxSocks)