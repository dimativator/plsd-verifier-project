import heapq
import sys
input = iter(sys.stdin.read().splitlines()).__next__


def solve():
    n, m, x = map(int, input().split())
    h = list(map(int, input().split()))
    # greedy; put on shortest tower
    towers = [(0, i+1) for i in range(m)]
    y = []
    for h_i in h:
        height, tower = heapq.heappop(towers)
        y.append(tower)
        heapq.heappush(towers, (height+h_i, tower))
    return " ".join(map(str, y))

t = int(input())
output = []
for _ in range(t):
    output.append("YES")
    output.append(solve())
print(*output, sep="\n")
