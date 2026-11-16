
# We are the all singing all dancing crap of the world

n = int(input()) 

khela = []
for i in range(n):
    s = input()
    khela.append([len(s),s])
    
khela = sorted(khela)    
if (n==1):
    print('YES')
    print(khela[0][1])
    
else:    
    lent = len(khela)
    for i in range(lent-1):
        c = 0
        for ii in range(i+1,khela[i+1][0]-khela[i][0]+2+i):
    #        print('i is ', 
    #                 i, 'ii is ',ii, '',khela[i][1],'== ??', khela[i+1][1][ii-i-1:ii+khela[i][0]-i-1])
    #          
            if (khela[i][1]==khela[i+1][1][ii-i-1:ii+khela[i][0]-i-1]):
                c = 1
        if c==0:
            break
        
    if c == 1:
        print("YES")
        for i in range(len(khela)):
            print(khela[i][1])
    
    else:
        print('NO')        
                    
                    
            
        
    
    








