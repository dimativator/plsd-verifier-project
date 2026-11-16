from sys import stdin

Modulo = 10 ** 9 + 7
n = int(stdin.readline())
p = map(int, stdin.readline().split())
son = [[] for i in xrange(n)]
dp = [[0, 0] for i in xrange(n)]
for i, x in enumerate(p, 1):
	son[x - 1].append(i)

for i in xrange(n - 1, -1, -1):
	t0, t1 = 0, 1
	for j in son[i]:
		t0, t1 = (t0 + t0 * dp[j][0] + t1 * dp[j][1]) % Modulo, (t1 + t1 * dp[j][0] + t0 * dp[j][1]) % Modulo
	r0, r1, d0, d1 = 0, 1, 0, 1	
	for j in reversed(son[i]):
		d0, d1 = (d0 + d1 * dp[j][1]) % Modulo, (d1 + d0 * dp[j][1]) % Modulo
		r0, r1 = (r0 + r0 * dp[j][0] + r1 * dp[j][1]) % Modulo, (r1 + r1 * dp[j][0] + r0 * dp[j][1]) % Modulo

	d1 = 1
	for j in son[i]:
		d1 = (d1 + d1 * dp[j][0]) % Modulo

	dp[i][0], dp[i][1] = (t0 + r0 - d0 + Modulo) % Modulo, (t1 + r1 - d1 + Modulo) % Modulo

print (dp[0][0] + dp[0][1]) % Modulo

