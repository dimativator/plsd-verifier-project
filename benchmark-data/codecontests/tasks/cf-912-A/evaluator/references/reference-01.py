y,b=input().split(' ')
ay,ag,ab=input().split(' ')
y=int(y)
b=int(b)
ay=int(ay)
ag=int(ag)
ab=int(ab)
b=b-(ab*3)
y=y-(ay*2)
b=b-ag
y=y-ag
br=0
if(y<0):
	br=br-y
if(b<0):
	br=br-b
print(br)