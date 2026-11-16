n=int(input())
s=input()
arr,k=[],0
for i in range(len(s)):
    if(s[i]=='B'):
        k+=1
    else:
        if(k>0):
            arr.append(k)
            k=0
if(k>0):
    arr.append(k)
print(len(arr))
print(*arr,sep=' ')