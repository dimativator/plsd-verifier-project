s = list(input())
d = {'a', 'u', 'o', 'e', 'i', '1', '3', '5', '7', '9'}
ans = 0
for i in s:
    if i in d:
        ans += 1
print(ans)
