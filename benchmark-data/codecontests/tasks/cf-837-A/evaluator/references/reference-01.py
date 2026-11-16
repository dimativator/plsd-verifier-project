n = int(input())
text = input()
ll = list(text.split())
num = []
for i in range(len(ll)):
    num.append(sum(1 for c in ll[i] if c.isupper()))
print(max(num))


 	 		  	  	 	 		 			  			 	 			