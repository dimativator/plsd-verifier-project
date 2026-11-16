
#make a table
n,m = map(int,input().split())
arr = [[] for i in range(n+1)]
for i in range(1,m+1):
    l = list(map(int,input().split()))
    arr[l[0]].append((l[1],l[2]))
    arr[l[1]].append((l[0],l[2]))


#dfs
def dfs(a,b,k):
    if a == b:
        return True
    seen.append(a)
    for i in arr[a]:
        x,c = i
        if c == k and x not in seen:
            if dfs(x,b,k):
                return True
    return False
    
query = int(input())
count = 0
score = [0]*(query)
seen = []
#get destination inputs
for i in range(query):
    a,b = map(int,input().split())
    for k in range(1,101):
        seen = []
        if dfs(a,b,k):
            count += 1
    score[i] = count
    count = 0

print("\n".join(list(map(str,score))))