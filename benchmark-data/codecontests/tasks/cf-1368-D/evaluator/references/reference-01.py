from sys import stdin
input = stdin.readline
n = int(input())
a = [*map(lambda x: bin(int(x))[:1:-1], input().split())]
c1 = len(max(a, key=len))
a = [x + '0' * (c1 - len(x)) for x in a]
b = [sum(c[i] == '1' for c in a) for i in range(c1)]
c2 = max(b)
ans = 0
for i in range(c2):
	num = ''
	for i in range(c1):
		if b[i] != 0:
			b[i] -= 1
			num += '1'
		else:
			num += '0'
	ans += int(num[::-1], 2) ** 2
print(ans)