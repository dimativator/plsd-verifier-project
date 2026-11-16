num = input()
sec = list(map(int, input().split(' ')))
ans = 0
def check(index):
    total = 1
    #print(sec[index])
    for i in range(len(sec)):
        #print(i)
        if index-i-1 < 0:
            break
        if sec[index-i-1] <= sec[index-i]:
            #print(i)
            total = total +1
        else:
            break
    for i in range(len(sec)):
        #print(i)
        if index+i+1 > len(sec)-1:
            break
        if sec[index+i+1] <= sec[index+i]:
            total = total + 1
        else:
            break
    return total

anslist = []
for i in range(len(sec)):
  anslist.append(check(i))
print(max(anslist))
#print(anslist)
#print(check(0))
