n = int(input())
counter= 0
for i in range(n):
	if input().find('+') > -1:
		counter = counter + 1
	else:
		counter = counter - 1
print(counter)