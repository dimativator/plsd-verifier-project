c1,c2,x,y=map(int,input().split())
def fn(val):
    f=[val//x,val//y]
    both=val//(x*y)
    f=[i-both for i in f]
    oth=val-f[0]-f[1]-both
    cnt=[c1-f[1],c2-f[0]]
    if cnt[0]<0:cnt[0]=0
    if cnt[1] < 0: cnt[1] = 0
    return (sum(cnt)<=oth)
l=0;r=int(1e18)
while r-l>1:
    m=(r+l)//2
    if fn(m):
        r=m
    else:l=m
print(r)