n, k = map(int, input().split())
a = list(map(int, input().split()))
aria = 0
bran = 0

for i in range(n):
    aria += a[i]
    
    if aria > 8:
        bran += 8
        aria -= 8
    else:
        bran += aria
        aria = 0

    if bran >= k:
        print(i + 1)
        break

if bran < k:
    print(-1)
