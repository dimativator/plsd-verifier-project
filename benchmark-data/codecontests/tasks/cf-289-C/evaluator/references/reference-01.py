def fastio():
	import sys
	from io import StringIO 
	from atexit import register
	global input
	sys.stdin = StringIO(sys.stdin.read())
	input = lambda : sys.stdin.readline().rstrip('\r\n')
	sys.stdout = StringIO()
	register(lambda : sys.__stdout__.write(sys.stdout.getvalue()))
fastio()

MOD = 10**9 + 7
I = lambda:list(map(int,input().split()))

n, k = I()
c = [chr(i + 97) for i in range(k)]
if n < k or (k == 1 and n > 1):
	print(-1)
	exit()
if n == 1:
	print(c[0])
	exit()
m = n - k + 2
ans = 'ab'*(m//2) + 'a'*(m%2)
print(ans + ''.join(c[2:]))