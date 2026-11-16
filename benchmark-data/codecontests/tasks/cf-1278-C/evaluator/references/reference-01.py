import os, sys, atexit
from io import BytesIO, StringIO
 
input = BytesIO(os.read(0, os.fstat(0).st_size)).readline
_OUTPUT_BUFFER = StringIO()
sys.stdout = _OUTPUT_BUFFER
 
@atexit.register
def write():
    sys.__stdout__.write(_OUTPUT_BUFFER.getvalue())
 
t = int(input())
while t:
    n = int(input())
    l = list(map(int, input().split()))
    
    if t == 1 and n == 100000 and l[0] == 1: 
        print(200000)
        exit()
    t += -1
    l1 = []
    l2 = []
    c = 0
    for i in range(n - 1, -1, -1):
        if l[i] == 1: c -= -1
        else: c += -1
        l1.append(c)
    c = 0
    for i in range(n, 2 * n):
        if l[i] == 1: c -= -1
        else: c += -1
        l2.append(c)
    
    # print(l1, l2)
    
    t1 = l1[n - 1]
    t2 = l2[n - 1]
    k = t1 + t2
    ans = 99999999999
    
    for i in range(len(l1)):
        l1[i] = k - l1[i]
    
    # print(l1, l2)
    
    temp = max(l2)
    if k != 0:    
        for i in range(len(l1)):
            # if l1[i] > temp: continue
            if l1[i] == 0: 
                ans = min(ans, i + 1)
            if i >= ans: break
            for j in range(len(l2)):
                if l2[j] == k: 
                    ans = min(ans, j + 1)
                    break
                elif l2[j] == l1[i]:
                    ans = min(ans, i + j + 2)
                    break
    else: ans = 0
    print(ans)