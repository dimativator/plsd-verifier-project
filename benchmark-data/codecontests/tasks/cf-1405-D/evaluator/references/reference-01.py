for t in range(int(input())):
	n, a, b, da, db = map(int, input().split())
	graph = [set() for i in range(n + 1)]
	for i in range(n - 1):
		u, v = map(int, input().split())
		graph[u].add(v)
		graph[v].add(u)

	visited = {1}
	last_visits = set()
	visit_now = {1}

	while len(visited) < n:
		while visit_now:
			i = visit_now.pop()
			last_visits |= graph[i] - visited
			visited |= graph[i]
		visit_now = last_visits
		last_visits = set()
	last = visit_now.pop()


	visited = {last}
	last_visits = set()
	visit_now = {last}

	N = 1
	while len(visited) < n:
		N += 1
		while visit_now:
			i = visit_now.pop()
			last_visits |= graph[i] - visited
			visited |= graph[i]
		visit_now = last_visits
		last_visits = set()

	

	
	visited = {a}
	last_visits = set()
	visit_now = {a}

	dist = 0
	while not b in visit_now:
		dist += 1
		while visit_now:
			i = visit_now.pop()
			last_visits |= graph[i] - visited
			visited |= graph[i]
		visit_now = last_visits
		last_visits = set()

	# print(f'N: {N}, Last: {last}, Dist AB: {dist}')
	if db < (2*da + 1):
		print('Alice')
	elif (2*da + 1) >= N:
		print('Alice')
	elif dist <= da:
		print('Alice')
	else:
		print('Bob')