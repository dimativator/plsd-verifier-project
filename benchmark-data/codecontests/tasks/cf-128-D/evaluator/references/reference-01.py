n=int(input())
g={}
for i in list(map(int,input().split())):g[i]=g.get(i,0)+2
mx=max(g)
for i in sorted(g)[:-1]:
	if i+1 not in g:exit(print('NO'))
	g[i+1]-=g[i]
	if g[i+1]<0:exit(print('NO'))
print('YES'if g[mx]==0 and list(g.values()).count(0)==1else'NO')