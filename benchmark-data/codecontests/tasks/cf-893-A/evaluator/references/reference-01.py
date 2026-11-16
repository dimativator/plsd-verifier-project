num=int(input())
spectator=3
p1=1
p2=2
yes=True
for i in range(0,num):
    winner=int(input())
    if winner is spectator:
        print("NO")
        yes=False
        break
    if p1 is winner:
        temp=spectator
        spectator=p2
        p2=temp
    else:
        temp=spectator
        spectator=p1
        p1=temp
if yes:
    print("YES")
