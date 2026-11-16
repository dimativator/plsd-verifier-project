n = int(input())
segments = []
minl = 10**9
maxr = 1

for i in range(n):
    a, b = map(int, input().split())
    segments.append((a, b))
    if a<minl:
        minl = a
    if b>maxr:
        maxr = b
        
if (minl, maxr) in segments:
    print(segments.index((minl, maxr))+1)
else:
    print(-1)
    
    
