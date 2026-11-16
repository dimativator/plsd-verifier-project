def main():
	n = int(input())
	pairs = []
	for i in range(n-1):
		a, b = list(map(int, input().split()))
		pairs.append([a-1, b-1])

	colors = list(map(int, input().split()))


	bad_pairs_count = 0
	bad_points_counts = {0:0}
	for a,b in pairs:
		if colors[a] != colors[b]:
			bad_pairs_count += 1
			def add(x):
				if x not in bad_points_counts:
					bad_points_counts[x] = 0
				bad_points_counts[x] += 1
			add(a)
			add(b)
		

	for k, v in bad_points_counts.items():
		if v == bad_pairs_count:
			print("YES")
			print(k+1)
			return
	print("NO")

main()

