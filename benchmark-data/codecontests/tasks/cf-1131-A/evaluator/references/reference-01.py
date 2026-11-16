w1, h1, w2, h2 = map(int, input().split())

if w2 > w1:
    res = w1 + 1 +  h1 + h2 + 1 + w2  + 1 + h2 + (w1 - w2) + h1 + 1
else:
    res = (w1 + h1 + h2) * 2 + 4

print(res)