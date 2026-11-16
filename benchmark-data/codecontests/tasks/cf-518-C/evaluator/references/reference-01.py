'''input
5 4 2
3 1 5 2 4
4 4 4 4
'''
import math
from sys import stdin, stdout


def get_order(pemut):
	order = dict()
	for i in range(1, n + 1):
		order[permut[i - 1]] = i 

	r_order = dict()
	for i in order:
		r_order[order[i]] = i

	return order, r_order


# main starts
n, m, k = list(map(int, stdin.readline().split()))
permut = list(map(int, stdin.readline().split()))
order, r_order = get_order(permut)
# print(order, r_order)
barr = list(map(int, stdin.readline().split()))
ans = 0
for num in barr:
	# print(math.ceil(order[num] / k))
	# print(order, r_order)
	ans += math.ceil(order[num] / k)
	if order[num] != 1:
		temp = r_order[order[num] - 1]
		temp2 = order[num]
		order[num] = order[num] - 1
		r_order[temp2] = temp
		r_order[temp2 - 1] = num
		order[temp] = temp2
print(ans)
