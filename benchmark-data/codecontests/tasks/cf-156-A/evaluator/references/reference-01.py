from sys import stdin, stdout

first, second = stdin.readline().strip(), stdin.readline().strip()
n, m = len(first), len(second)

first = '#' * m + first + '#' * m
ans = float('inf')

for i in range(n + m):
    cnt = 0
    
    for j in range(m):
        if first[i + j] != second[j]:
            cnt += 1
    
    ans = min(cnt, ans)

stdout.write(str(ans))