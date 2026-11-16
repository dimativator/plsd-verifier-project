x, y = input().split(" ")
a = x,y
a = list(a)
for i in range(len(a)):
    a[i]=int(a[i])
count=0
num =a[1]
for i in range(a[0]):
    z,f = input().split(" ")
    char=z
    inp=int(f)
    if char == '+':
        num = num + inp
    elif char == '-':
        num = num - inp
        if num < 0:
            count+=1
            num = num+inp

print(num,count)


   	 	   	 	   	  		 			     		