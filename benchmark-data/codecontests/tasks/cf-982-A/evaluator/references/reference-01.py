n = int(input())
l = '0' + input() +'0'
o = 0
z = 0
flag = True
for i in l:
    if i == "0" and z < 2:
        z += 1
        o = 0
    elif i == "1" and o != 1:
        o = 1
        z = 0
    else:
        flag = False
        break
if flag:
    print("Yes")
else:
    print("No")
