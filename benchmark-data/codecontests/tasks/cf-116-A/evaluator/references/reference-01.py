n = int(input())

tram = []
current = []

curr = 0

for i in range(0, n):
    tram.extend([int(x) for x in input().split()])

for i in range(0, 2*n, 2):
    curr -= tram[i]
    curr += tram[i+1]
    current.append(curr)
print(max(current))
