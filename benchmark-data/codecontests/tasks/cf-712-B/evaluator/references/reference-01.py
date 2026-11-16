s = input()
ud = lr = 0
for ch in s:
    if(ch=='R'):
        lr = lr+1
    if(ch=='L'):
        lr = lr-1
    if(ch=='U'):
        ud = ud+1
    if(ch=='D'):
        ud = ud-1

if((abs(lr) + abs(ud))%2==1):
    print(-1)
else:
    print(int((abs(lr) + abs(ud))/2))

