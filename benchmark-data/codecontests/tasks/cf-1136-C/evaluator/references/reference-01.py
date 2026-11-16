import os
from io import BytesIO
input = BytesIO(os.read(0, os.fstat(0).st_size)).readline

from collections import defaultdict

def main():
    n, m = map(int, input().split())
    s1 = [defaultdict(int) for _ in range(n + m)]
    s2 = [defaultdict(int) for _ in range(n + m)]

    for s in (s1, s2):
        for i in range(n):
            for j, x in enumerate(input().split()):
                x = int(x)
                s[i + j][x] += 1
                
    if all(d1 == d2 for d1, d2 in zip(s1, s2)):
        print("YES")
    else:
        print("NO")

main()