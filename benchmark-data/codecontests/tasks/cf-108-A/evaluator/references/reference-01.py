s=input()
if s[0]=="0":
    h=s[1]
else:
    h=s[:2]
if s[3]=="0":
    m=s[3]
else:
    m=s[3:]
def pallin(x,y):
    if len(x)==1:
        x="0"+x
    if len(y)==1:
        y="0"+y
    if x[0]==y[1] and x[1]==y[0]:
        return True
    else:
        return False
while(1):
    if int(m)+1==60:
        h=str((int(h)+1)%24)
        m=str(0)
    else:
        m=str(int(m)+1)
    if pallin(h,m):
        if len(h)==1:
            h="0"+h
        if len(m)==1:
            m="0"+m
        print(h+":"+m)
        break
    
        
    