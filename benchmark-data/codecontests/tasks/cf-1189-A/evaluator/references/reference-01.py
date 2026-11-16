n = int(input())
s = str(input())
c = 0
for i in range(len(s)):
    if s[i]=='0':
        c+=1
    else:
        c-=1

if c!=0:
    print("1"+ "\n" + s)
else:
    print("2" + "\n" + s[0:-1],s[-1])