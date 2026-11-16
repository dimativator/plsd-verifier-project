n = int(input())
l = [int(x) for x in input().split()]
s = ''
for x in l[:-1]:
	if x:
		s += 'P'
		for i in range(x - 1):
			s += 'RLP'
	s += 'R'
if l[-1]:
	s += 'P'
	for i in range(l[-1] - 1):
		s += 'LRP'
print(s)
