T = int(input())
for t in range(T):
    a = [int(x) for x in list(input())]
    if sum(a)%3==0 and a.count(0)>0 and (a.count(0)+a.count(2)+a.count(4)+a.count(6)+a.count(8)>1):
        print("red")
    else:
        print("cyan")