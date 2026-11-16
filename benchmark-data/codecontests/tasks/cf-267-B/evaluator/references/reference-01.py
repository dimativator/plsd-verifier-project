


def euler(start):
    s = [(start,0)]
    ans = []
    while s:
        i,e = s[-1]
        if i in mark:
            mark.remove(i)
        if degree[i]==0:
            ans.append(e)
            s.pop()
        else:
            for j,e in graph[i]:
                if vis[abs(e)]==0:
                    degree[i]-=1
                    degree[j]-=1
                    vis[abs(e)]=1
                    s.append((j, e))
                    break
    #ans.reverse()
    if mark:
        print("No solution")
    else:
        for i in ans:
            if i<0:
                print(-i,"+")
            elif i>0:
                print(i, "-")



n = int(input())
degree = [0]*7
vis    = [0]*(n+1)
graph = [[] for _ in range(7)]
start = 0
mark = set()
for i in range(1,1+n):
    x,y = map(int, input().split())
    graph[x].append((y,  i))
    graph[y].append((x, -i))
    degree[x]+=1
    degree[y]+=1
    mark.add(x)
    mark.add(y)
    start = x
odd  =0


for i in range(0,7):
    if degree[i]%2==1:
        odd+=1
        start=i


if odd not in [0,2]:
    print("No solution")
else:
    euler(start)
