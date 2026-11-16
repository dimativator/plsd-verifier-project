def dfs(G, start, path_exists):
    s = [start]
    visited = set([])
    if not start in path_exists:
        path_exists[start] = set([])

    while(s):
        node = s.pop()
        if not node in visited:
            visited.add(node)
            path_exists[start].add(node)
            a, b = G[node]

            for i, (c, d) in enumerate(G):
                if i != node:
                    if i in path_exists[start] or (c < a < d) or (c < b < d):
                        s.append(i)

if __name__ == "__main__":
    n = int(input())

    G = []
    path_exists = {}
    for _ in range(n):
        q, a, b = map(int, input().split())
        
        if q == 1:
            G.append((a, b))
        else:
            a -= 1
            b -= 1
            dfs(G, a, path_exists)
            if b in path_exists[a]:
                print("YES")
            else:
                print("NO")
