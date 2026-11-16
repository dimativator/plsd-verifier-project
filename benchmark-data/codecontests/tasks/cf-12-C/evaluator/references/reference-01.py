n, m = input().split(" ")
n = int(n)
m = int(m)
priceList = []
res = []
least = 0
most = 0
fruitCount = 0
seq = input().split(" ")
for i in seq:
    priceList.append(int(i))
    
item = []
count = []

for i in range(m):
    inp = input()
    if inp in item:
        count[item.index(inp)] += 1
    else:
        item.append(inp)
        count.append(1)
        fruitCount += 1
        
count.sort()
count.reverse()
priceList.sort()

for i in range(len(count)):
    least += priceList[i] * count[i]

res.append(str(least))

priceList.reverse()



for i in range(len(count)):
    most += priceList[i] * count[i]

res.append(str(most))

print(" ".join(res))
  			 		      	   				    	  		