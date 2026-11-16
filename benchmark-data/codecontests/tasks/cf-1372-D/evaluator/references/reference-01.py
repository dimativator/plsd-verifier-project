n = int(input())
a = [int(x) for x in input().split()]
if n == 1:
	print(a[0])
	exit()
evens = [a[0]]
odds = [a[1]]
for i in range(2,n):
	if i % 2 == 0:
		evens.append(evens[-1]+a[i])
	else:
		odds.append(odds[-1] + a[i])
# print(evens)
# print(odds)
maxi = 0
for i in range(len(evens)):
	score = evens[i]
	if i == 0:
		score += odds[-1]
	else:
		score += odds[-1] - odds[i-1]
	if score > maxi:
		maxi = score
for i in range(len(odds)):
	score = odds[i]
	score += evens[-1] - evens[i]
	if score > maxi:
		maxi = score
print(maxi)