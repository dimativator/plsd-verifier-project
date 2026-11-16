sizes=[int(x) for x in str(input()).split(" ")]
l=(sizes[0],2*sizes[0])
m=(max(2*sizes[3]+1,sizes[1]),2*sizes[1])
s=(max(sizes[2],sizes[3]),min(2*sizes[2],2*sizes[3]))

if m[1]>=m[0] and s[1]>=s[0]:
    print(l[1])
    print(max(m[0],s[0])+1)
    print(s[0])
else:
    print(-1)
