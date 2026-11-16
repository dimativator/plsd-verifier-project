check = lambda ax, ay, bx, by, cx, cy : bx + cx <= ax and max(by, cy) <= ay
inp = lambda : map(int, input().split())
x1, y1 = inp()
x2, y2 = inp()
x3, y3 = inp()
if check(x1, y1, x2, y2, x3, y3) or check(y1, x1, x2, y2, x3, y3) or check(x1, y1, y2, x2, x3, y3) or check(y1, x1, y2, x2, x3, y3) or check(x1, y1, x2, y2, y3, x3) or check(y1, x1, x2, y2, y3, x3) or check(x1, y1, y2, x2, y3, x3) or check(y1, x1, y2, x2, y3, x3):
    print("YES")
else:
    print("NO")
