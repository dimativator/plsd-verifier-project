from sys import stdin
from collections import *


class graph:
    def __init__(self):
        self.gdict = defaultdict(list)

    def addEdge(self, node1, node2, w=None):
        self.gdict[node1].append(node2)
        self.gdict[node2].append(node1)

    def subtree(self, v):
        queue, visit, ans = deque([v]), [False] * (n + 1), []
        visit[v], self.nodes = True, [0] * (n + 1)
        for i in a:
            self.nodes[i] = 1

        while queue:
            s = queue.popleft()

            for i in self.gdict[s]:
                if not visit[i]:
                    queue.append(i)
                    visit[i] = True
                    ans.append((i, s))
        res = 0
        while ans:
            i, j = ans.pop()
            self.nodes[j] += self.nodes[i]
            res += min(self.nodes[i], 2 * k - self.nodes[i])
        print(res)


rints = lambda: [int(x) for x in stdin.readline().split()]
n, k = rints()
a, g = rints(), graph()
for _ in range(n - 1):
    u, v = rints()
    g.addEdge(u, v)
g.subtree(1)
