n = int(input())
a = int(input())
b = int(input())
for i in range(n//a+1):
  if (n - i * a) % b == 0:
    print("YES")
    print(i, (n - i * a) // b)
    break
else: print("NO")
  	  		  	            	   	  	