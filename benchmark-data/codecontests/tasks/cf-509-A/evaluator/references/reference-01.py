n = int(input())
list1 = []
list2 = [1 for i in range(n)]
list3 = [1] + [0 for i in range(n-1)]
list1.append(list2)
for i in range(n-1):
    list1.append(list3)
for i in range(1,n):
    for j in range(1,n):
        list1[i][j] = list1[i-1][j] + list1[i][j-1]
list4 = []
for i in range(n):
    list4.append(max(list1[i]))
print(max(list4))