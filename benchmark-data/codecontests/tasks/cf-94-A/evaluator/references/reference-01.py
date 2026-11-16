s = input()
a = []
for i in range(10):
    a.append(input())

p = 0
while(p < 80):
    for i in range(10):
        if a[i] == s[p:p+10]:
            print(i, end='')
            p += 10
            break

