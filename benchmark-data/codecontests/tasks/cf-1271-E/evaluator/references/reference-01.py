n, k = map(int,input().split())
p = 1 
w = 0
while p * 2 <= k:
	p *= 2
	w += 1
kk = k - p
#2**w * tr <= n - kk
odd = (n-kk)//2**w
if odd % 2 == 0:
	odd -= 1

p = 1
w = 0
while 2 * (2*p - 1) < k:
	p *= 2
	w += 1
poz = k - 2*(p-1)
if poz == 0:
	#2**(w-1) * strzal + (2**w-1) <= n
	even = (n-(2**w-1))//2**(w-1)
	if even % 2 == 1:
		even -= 1
else:
	if poz <= p*4343:
		#porownanie z zerem na koncu
		strzal = (n+1-poz)//p
		if strzal % 2 == 1:
			strzal -= 1
	even = strzal
print(max(even,odd))
