import math
result = []
cases = int(input())

for i in range(cases):
    sum = 0
    num = int(input())
    ain = list(map(int,input().split(" ")))
    dt = {}
    dt[0]=0
    dt[1]=0
    dt[2]=0
    for j in ain:
        dt[j%3]=dt[j%3]+1
    for l in range(2):
        for m in range(3):
            if dt[m]>num/3:
                diff = dt[m]-num/3
                dt[m]=num/3
                dt[(m+1)%3]+=diff
                sum+=diff
    result.append(int(sum))

for _ in result:
    print(_)