n, m, k = list(map(int,input().split()))
tooth = [[0,True]] * n
for i in range(n):
  r, c = list(map(int,input().split()))
  if tooth[r-1][0] > c or tooth[r-1][1] == True:
    tooth[r-1] = [c,False]
ad = 0
for i in tooth:
  ad += i[0]
print(min(ad,k))