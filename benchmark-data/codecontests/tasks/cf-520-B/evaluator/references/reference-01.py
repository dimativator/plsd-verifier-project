n, m = [int(x) for x in input().split()]
s = 0

while(n < m):
    s += 1 + (m % 2)
    m = (m + m % 2) // 2

print(s + n - m)
