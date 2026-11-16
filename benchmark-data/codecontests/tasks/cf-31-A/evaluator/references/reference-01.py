n = int(input())
line = list(map(int,input().split()))
for i in range(n-1):
    for j in range(i+1,n):
        if line[i] + line[j] in line:
            print(line.index(line[i] + line[j])+1, i+1, j+1)
            exit(0)
print('-1')