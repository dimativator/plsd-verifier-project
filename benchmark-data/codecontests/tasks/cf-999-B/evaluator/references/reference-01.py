l = int(input())
s = list(input())

for i in range(2, l + 1):
    if l % i > 0: continue
    s[:i] = s[i - 1::-1]
print(''.join(s))
