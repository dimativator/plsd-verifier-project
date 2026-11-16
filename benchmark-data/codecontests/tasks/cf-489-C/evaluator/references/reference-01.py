m,s = list(map(int,input().split()))
flag = True
large = 0
small = 0
m1 = m-1
m2 = 0
s1 = s
if s==0 and m==1:
	small,large = 0,0
	flag = False
elif s>9*m or s<1:
	flag = False
	large = -1
	small = -1
if flag:
	while (s1 != 0):
		if s1 >9:
			large += 9*10**(m1)
			small += 9*10**(m2)
			s1 -= 9
			m1 -= 1
			m2 += 1
		else:
			large += s1 * 10 **(m1)
			if m2 == m - 1:
				small += s1 * 10**(m2)
			else:
				small += 10 **(m-1)
				small += (s1 -1)*10**m2

			s1 = 0

	# while (s != 0):
	# 	m1 = 0
	# 	if s >= 9:
	# 		small += 9*10**m1
	# 		s -= 9
	# 		m1 += 1
	# 	else:
	# 		if m1 == m-1:
	# 			small += s * 10**m1
	# 			s =0
	# 		else:
	# 			small += 10**(m-1)
	# 			s-= 1
	# 			small += s*10**m1
	# 			s = 0
	# if (s/9 == m):
	# 	small = large
	# elif (s%9 == 0):
	# 	m1 = m-1
	# 	zero = m - s//9
	# 	while (s!= 0):
	# 		if zero >= 1:
	# 			small += 10**m1
	# 			zero -= 1
	# 			m1 -= 1
	# 			s -= 1
	# else:
	# 	m1 = m-1
	# 	tmp = large
	# 	while(tmp != 0):
	# 		digit = tmp%10
	# 		small += digit*10**m1
	# 		m1 -= 1
	# 		tmp //=10
print(small,large)
