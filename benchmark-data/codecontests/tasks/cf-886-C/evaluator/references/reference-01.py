c = int(input())
a = list(map(int, input().split()))
res = 0
b = []
for i in range(len(a)):
    b.append(False)
for i in range(len(a)):
    k = len(a) - i - 1   
    m = 0
    while b[k] == False:
        b[k] = True
        k = a[k] - 1
        m = 1
        if (k == -1):
            break  
    if m == 1:
        res = res + 1
print(res)