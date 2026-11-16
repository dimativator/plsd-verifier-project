import math

h, l = input().split()
h = int(h)
l = int(l)
a = float((pow(l,2)-pow(h,2))/(2*h))
print(a)