import math
a = input()
d = int(max(a))
print(d)
dec = math.ceil(math.log10(int(a)))
c = [0]*d
if int(a) != 10**dec:
    for i in a:
        for j in range(int(i)):
            c[j] = c[j]+10**(dec-1)
        dec = dec - 1
d=''
for i in c:
    d += str(i)+' '
if int(a) == 10**dec:
    print(a)
else:
    print(d.strip())