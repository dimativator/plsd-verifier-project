def fast_exp_pow(num, pw, mod):
	num %= mod
	if pw == 1:
		return num
	evener = 1
	if pw % 2 == 1:
		evener = num
	return (evener * (fast_exp_pow(num, pw // 2, mod) % mod) ** 2) % mod


mod = 1000000007
n = int(input())
if n == 1:
	print(0)
	quit()
x = ((fast_exp_pow(3, n - 1, mod) + (-1) ** (n & 1) + mod) * 3) % mod
y = 250000002
print((x * y) % mod)
