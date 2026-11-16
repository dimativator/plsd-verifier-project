t = int(input())
for _ in range(t):
    n = int(input())
    for j in range(n):
        b = [0] * n
        b[j] = 1
        b[-j-1] = 1
        if j != (n-1) and j != (n//2):
            print(*b)
        else:
            if n % 2 == 0:
                print(*b)
            else:
                if j == (n-1):
                    b[n//2] = 1
                    print(*b)
                if j == (n//2):
                    b[n//2 - 1] = 1
                    print(*b)
            
    
        
        
            
        
    
        
                
        
                
            
    
    
    
    
        
        
        
        
    
        
        
        
    
        
                
    
        
        
            
        
        
    
    
    
            
        
    
            
        
    
        
    
            
        
    
    
        
            
    
    
        
    
        
            
            
            
        
            
            
            
            
            
            

    
        
        
        
        
    
    
        
            
    
        
        
                
            
            
            
            
    
            
                
        
        
    
            
    
        
            
        
    

    
    
    
           
        
        
        
            

        
    
        
    
    
    
