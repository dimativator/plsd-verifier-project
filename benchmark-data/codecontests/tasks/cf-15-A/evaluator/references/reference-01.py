n,t=list(map(int,input().split()))
amount=2
houses=[]
for i in range(n):
    c,l=list(map(int,input().split()))
    l=l/2
    start,end=c-l,c+l
    houses.append([start,end])

houses.sort(key=lambda x:x[0])
prev_end=houses[0][0]
for start,end in houses:
    gap=start-prev_end
    if gap>t:
        amount+=2
    elif gap==t:
        amount+=1
    prev_end=end
    
    
print(amount)
    
    
