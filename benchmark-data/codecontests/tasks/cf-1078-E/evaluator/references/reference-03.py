u = 'u'
d = 'd'
l = 'l'
r = 'r'

t = 't'
e = 'e'
v0 = '0'
v1 = '1'

def rev(x) : return 'lrud'['lrud'.find(x) ^ 1]
def copy(x) : return x + v1 + v0 + rev(x) + t

def make_leading(x):
	res = ''
	res += x * 2 + v0 + x + v1 + rev(x) * 2 + v1 + v0 + rev(x) + t
	res += x * 2 + t + x + e + x + e + rev(x) * 2
	res += rev(x) + v1 + v0 + x + t + x + e + rev(x)
	return res

def xor_gate():
	return v0 + v1 + v0 + u + t + l + t

def calc_xor():
	return u + copy(u) * 2 + d * 3 + copy(u) * 2 + copy(l) + r + xor_gate() + copy(d) + d

def add_up():
	return calc_xor() + v0 + u + l + r + t + d + calc_xor() + l * 2 + t + r

def add_bit():
	res = ''
	res += u + copy(u) + copy(l) + l + v0 + l + v1 + r * 3 + add_up()
	res += d * 2 + copy(u) + copy(u) + copy(l) + r + add_up()
	return res + d * 2

def work(n):
	res = ''
	res += (make_leading(d) + l) * n + u
	res += (r + make_leading(u)) * n + u * 2
	res += (v0 + l) * (n + 1) + r * (n + 1) + d * 3
	res += (add_bit() + l) * n
	return res + u * 3

print work(32)
