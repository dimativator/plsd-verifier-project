n,c = map(int,input().split())
p=input().split()
t=input().split()
sl=0
sr=0
ti=0
for i in range(n):
    ti+=int(t[i])
    if int(p[i])-c*ti>=0:
        sl+=int(p[i])-c*ti
ti=0
for i in range(n):
    ti+=int(t[n-i-1])
    if int(p[n-i-1])-c*ti>=0:
        sr+=int(p[n-i-1])-c*ti
if sl == sr:
    print('Tie')
elif sl>sr:
    print('Limak')
else:
    print('Radewoosh')
