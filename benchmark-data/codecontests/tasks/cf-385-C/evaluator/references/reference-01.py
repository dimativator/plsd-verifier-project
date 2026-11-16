import math, sys

input = sys.stdin.buffer.readline

def ints():
    return map(int, input().split())

n = int(input())
x = list(ints())
MAX = max(x) + 1
freq = [0] * MAX
for i in x:
    freq[i] += 1

sieve = [False] * MAX
f = [0] * MAX
for i in range(2, MAX):
    if sieve[i]:
        continue
    for j in range(i, MAX, i):
        sieve[j] = True
        f[i] += freq[j]
for i in range(2, MAX):
    f[i] += f[i-1]

m = int(input())
for i in range(m):
    l, r = ints()
    if l >= MAX:
        print(0)
    elif r >= MAX:
        print(f[-1] - f[l-1])
    else:
        print(f[r] - f[l-1])