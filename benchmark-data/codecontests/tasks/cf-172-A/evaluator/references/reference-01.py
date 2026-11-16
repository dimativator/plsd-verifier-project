n = int(input())

phone = []

for i in range(n):
    s = input().strip()
    phone.append(s)

c = 0
k = 0
flag = True
while True:
    for p in phone:
        if p[k] != phone[0][k]:
            flag = False
            break
    k += 1

    if flag:
        c += 1
    else:
        print(c)
        break
