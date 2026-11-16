n , k = map(int,input().split())
n = list(str(n))
counter = 0
zero_counter = 0
if n.count('0') >= k :
	for i in range(len(n)-1 , -1 , -1):
		if (n[i] != '0'):
			counter += 1
		if (n[i] == '0'):
			zero_counter += 1
		if (zero_counter == k):
			break
	print(counter)  
else:  
  print(len(n) - 1)