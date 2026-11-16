t=eval(input())
for j in range(t):
    n=eval(input())
    if n==2 :
        print(2)
    else:
        sum=2
        for i in range(1,n//2):
            sum=sum+2**(i+1)
        print(sum)
            
				        		     	    		  	 	