t = int(input())
for _ in range(t):
	s = input()
	t = input()
	ok = False
	s = ''.join(sorted(s))
	for i in range(len(t) - len(s) + 1):
		temp = ''.join(sorted(t[i:i+len(s)]))
		if temp == s:
			ok = True
			break
	if ok:
		print("YES")
	else:
		print("NO")

