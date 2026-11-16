n = int(input())
s = input()

i,p=0,1
ans = ''
while i<(n-1):
    if p%2 == 1:
        if s[i] != s[i+1]:
            ans = ans + s[i]
            p += 1
    else:
        ans = ans + s[i]
        p += 1

    i += 1

if len(ans)%2 == 1:
    ans += s[-1]
print(len(s)-len(ans))
print(ans)

