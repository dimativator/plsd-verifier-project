n = int(input())
fi = list(map(int, input().split()))
fi2 = list(range(n))
i = 0
while i < n:
  fi2[fi[i] - 1] = i
  i += 1
pos = fi2[0]
i = 1
d = 0
while i < n:
  d += abs(fi2[i] - pos)
  pos = fi2[i]
  i += 1
print(d)
