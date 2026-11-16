#***************14B - Young Photographer***************#
#author - @Divyesh Chhabra

from math import *
import os
import random
import re
import sys
from itertools import *

n,a = map(int,input().split())
sp = []
xp = []
yp = []
f = 1
while n != 0:
    x,y = map(int,input().split())
    if x>y:
        x,y = y,x
    xp.append(x)
    yp.append(y)
    sp.append([x,y])
    n-=1
xp.sort()
yp.sort()
for i in xp:
    if yp[0]<i:
        f=0
        break
if f==0:
    print(-1)
elif a>=xp[len(xp)-1] and a<=yp[0]:
    print(0)
else:
    print(min(abs(xp[len(xp)-1]-a),abs(yp[0]-a)))
    