N, Q = map(int, input().split())
A = list(map(int, input().split()))
T = list(map(int, input().split()))
inds = [0]*51
for i in range(N):
  if inds[A[i]]==0:
    inds[A[i]] = i+1
ans = []
for i in range(Q):
  ans.append(inds[T[i]])
  for c in range(1,51):
    if inds[c]<inds[T[i]]:
      inds[c] += 1
  inds[T[i]] = 1
print(*ans)
