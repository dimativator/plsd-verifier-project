n,k=map(int,input().split())
l=list(map(int,input().split()))
rem=[]
ans=0
for i in l:
    rem.append(i%10)
    ans=ans+i//10
    #print(ans)
rem.sort()           #  0 1 2 3.. 9 9 9..
i=n-1
while(i>=0 and k>0):
    if(rem[i]!=0):       #starting from back  9 -> 8 .... -> 2 -> 1->0
        sm=10-(rem[i])
        if(k>=sm):
            k=k-sm
            rem[i]=0
            ans=ans+1
    #print(ans)
    i=i-1
    
#after coming out of while , either k==0, then some or all of rem values are 0 , it means actual value id div by 10
#if k>0 , it means all values are div by 10, so we can add 10 to get more max answer, and use them, until we reach n*10
print(min(ans + k//10 ,n*10))








