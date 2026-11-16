n, x1, y1, x2, y2 = map(int, input().split())
first, secnd = 0, 0
if y1 == 0:
    first = 4
elif y1 == n:
    first = 2


if x1 == 0:
    first = 1
elif x1 == n:
    first = 3

if y2 == 0:
    secnd = 4
elif y2 == n:
    secnd = 2
if x2 == 0:
    secnd = 1
elif x2 == n:
    secnd = 3


if first == 4 and secnd == 1:
    pass
elif first > secnd or (first == 1 and secnd == 4):
    x1, x2 = x2, x1
    y1, y2 = y2, y1
    first, secnd = secnd, first

if abs(first - secnd) == 1 or first + secnd == 5:
    if first == 1:
        rast = n - y1 + x2
    elif first == 3:
        rast = y1 + n - x2
    elif first == 2:
        rast = n - x1 + n - y2
    else:
        rast = x1 + y2
elif first == secnd:
    if first == 2 or first == 4:
        rast = abs(x1 - x2)
    else:
        rast = abs(y1 - y2)
else:
    if first == 1:
        rast = min(y1 + n + y2, n - y1 + n - y2 + n)
    else:
        rast = min(x1 + n + x2, n - x1 + n - x2 + n)
print(rast)