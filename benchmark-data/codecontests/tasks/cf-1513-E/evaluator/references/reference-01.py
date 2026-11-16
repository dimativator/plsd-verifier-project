n=int(input());a=*map(int,input().split()),;s=sum(a)
if s%n:print(0);exit(0)
M=10**9+7;s//=n;f=[1]*(n+1);b=[0]*3;d=dict()
for i in range(2,n+1):f[i]=f[i-1]*i%M
for x in a:
	b[(x>s)-(x<s)]+=1
	try:d[x]+=1
	except:d[x]=1
k=1
for x in d.values():k*=f[x]
k=f[n]*pow(k,M-2,M)
print([k%M,f[b[1]]*f[b[-1]]*2*pow(f[n-b[0]],M-2,M)*k%M][b[1]>1and b[-1]>1])