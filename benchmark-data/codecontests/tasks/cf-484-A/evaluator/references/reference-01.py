n = int(input())

for i in range(n):

    l,r=map(int,input().split())
    
    while(l|(l+1)<=r): # or make like max function here .
        l|=l+1  # or here like equal
        
    print(l)
