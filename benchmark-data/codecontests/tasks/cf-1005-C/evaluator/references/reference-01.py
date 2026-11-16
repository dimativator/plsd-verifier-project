from collections import*
input()
arr = Counter(map(int,input().split()))
binpow = [2**i for i in range(31)]
deleted = 0
for item in list(arr.elements()):
    flag = True
    for bp in binpow:
        if (arr.get(bp - item) != None):
            if (bp - item == item):
                if (arr.get(bp - item) > 1):
                    flag = False
                    break
            else:
                flag = False
                break
    if (flag):
        deleted += 1
print(deleted)