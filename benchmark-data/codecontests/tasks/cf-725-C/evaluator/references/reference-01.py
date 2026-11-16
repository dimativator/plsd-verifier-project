import sys

debug = False

def print_debug(*args, **kwargs):
    if debug:
        print(*args, **kwargs, file=sys.stderr)

s = input()

double = ''

for c in range(ord('A'), ord('Z')+1):
    if s.count(chr(c)) == 2:
        double = chr(c)

i1, i2 = [ i for i, c in enumerate(s) if c == double ]

print_debug(double, i1, i2)

if abs(i1 - i2) == 1:
    print("Impossible")
    sys.exit(0)

for shift in range(0, 26):
    i1, i2 = [ i for i, c in enumerate(s) if c == double ]
    s2 = s[:i1] + s[i1+1:]
    i1 -= 1
    print_debug(s2)
    i2 = [ i for i, c in enumerate(s2) if c == double ][0]
    print_debug(i2)
    i2 = 25-i2
    print_debug(i2)
    if i2-1 <= i1 <= i2:
        print(s2[:13])
        print(s2[13:][::-1])
        sys.exit(0)
    s = s[1:] + s[:1]

print("Impossible")

# 12-i1 == i2-14
# 26-i1-i2+x == 0
# shift = -((26-i1-i2)//2)
# print_debug(shift)
# s = s[shift:] + s[:shift]
# print_debug(s)
# print(s[0:13])
# print(s[13:26][::-1])

# line1 = s[i1:i2-(i2-i1)//2]
# line2 = s[i2-(i2-i1)//2:i2][::-1]
# line2 = s[i2+1:min(i2+1+13-len(line2), 27)][::-1] + line2
# if len(line2) < 13:
#     line2 = s[0:13-len(line2)][::-1] + line2


# print_debug(line1 + '\n' + line2)
#
# print(line1)
# print(line2)
