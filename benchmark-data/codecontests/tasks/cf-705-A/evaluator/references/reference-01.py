x = int(input())

feelings = ''
for _ in range(x):
	if _ == x - 1:
		if _ % 2 != 0:
			feelings = feelings + 'I love it '
		else:
			feelings = feelings + 'I hate it '
	else:
		if _ % 2 != 0:
			feelings = feelings + 'I love that '
		else:
			feelings = feelings + 'I hate that '	
print(feelings)

