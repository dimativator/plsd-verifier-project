from collections import defaultdict, deque
from sys import stdin, stdout 

def dfs(visited, node_idx, graph, color_count, sock_colors):
    visited[node_idx] = True
    color_count[sock_colors[node_idx]] += 1
    count = 1
    for nbor_idx in graph[node_idx]:
        if not visited[nbor_idx]:
            count += dfs(visited, nbor_idx, graph, color_count, sock_colors)
    return count

def bfs(visited, idx, graph, color_count, sock_counts):
    q = deque()
    q.append(idx)
    count = 0
    while len(q) != 0:
        _next = q.popleft()
        if visited[_next]:
            continue
        visited[_next] = True
        color_count[sock_colors[_next]] += 1
        count += 1
        for nbor_idx in graph[_next]:
            q.append(nbor_idx)

    return count
    

def disjoint(graph, sock_colors):
    total = 0
    visited = [False] * len(graph)
    for idx, nbors in enumerate(graph):
        color_count = defaultdict(int)
        if not visited[idx]:
            size = bfs(visited, idx, graph, color_count, sock_colors)
            total += size - max(color_count.values())

    return total

if __name__ == '__main__':
    num_socks, num_days, num_colors = list(map(int, stdin.readline().split(' ')))
    sock_colors = list(map(int, stdin.readline().split(' ')))
    graph = [[] for i in range(num_socks)]

    for i in range(num_days):
        a, b = list(map(int, stdin.readline().split(' ')))
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    ans = disjoint(graph, sock_colors)
    print(ans)
