a, b = input(), input()
ans = 0
index = a.find (b, 0)
while index != -1:
    ans = ans + 1
    index = a.find (b, index + len (b))
print (ans)
