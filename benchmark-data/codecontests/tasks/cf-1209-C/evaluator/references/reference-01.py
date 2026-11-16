for _ in range(int(input())):
	n = int(input())
	d = [*map(int, input())]
	s = d[:]
	s.sort()
	o = []
	i = 0
	ans = []
	for j in range(n):
		if d[j] == s[i]:
			ans.append('1')
			i += 1
		else:
			ans.append('2')
 
	t = []
     
	for i in range(n):
		if ans[i] == '1':
			t.append(d[i])
 
	for i in range(n):
		if ans[i] == '2':
			t.append(d[i])
 
	print(''.join(ans) if t == s else '-')