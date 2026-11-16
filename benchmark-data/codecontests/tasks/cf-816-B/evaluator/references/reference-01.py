ranges, maps, strs = range, map, str

fout = ""
count = 0

n, k, q = maps(int, input().split())
rangeArr = []

for i in ranges(200002):
	rangeArr.append(0)

for recipe in ranges(n):
	left, right = maps(int, input().split())

	rangeArr[left] += 1
	rangeArr[right + 1] -= 1

for recipe in ranges(1, len(rangeArr)):
	rangeArr[recipe] += rangeArr[recipe - 1]

	if rangeArr[recipe - 1] < k:
		rangeArr[recipe - 1] = 0
	else:
		rangeArr[recipe - 1] = 1

for i in ranges(1, len(rangeArr)):
    rangeArr[i] += rangeArr[i - 1]

for question in ranges(q):
	left, right = maps(int, input().split())

	fout += strs(rangeArr[right] - rangeArr[left - 1]) + "\n"

print(fout)