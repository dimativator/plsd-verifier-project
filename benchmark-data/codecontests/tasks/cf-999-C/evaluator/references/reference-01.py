# import collections
import string

letters = list(string.ascii_lowercase)
n, k = map(int, input().split())
a = list(input())

for i in range(n):
    a[i] = (i, a[i])

a.sort(key= lambda x: x[1])
a = a[k:]
a.sort(key= lambda x: x[0])

for i in range(len(a)):
    print(a[i][1], end='')