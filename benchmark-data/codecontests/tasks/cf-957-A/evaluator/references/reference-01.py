def complete_canvas(s):
    double = False
    res = ""
    for i,c in enumerate(s):
        if i>0 and i<len(s)-1 and c=='?' and s[i-1] in colors and s[i+1] in colors:
            #and s[i-1]!=s[i+1]
            col = list(colors)
            col.remove(s[i-1])
            if s[i-1]!=s[i+1]:
                col.remove(s[i+1])
            if s[i-1]==s[i+1]:
                double = True
            res += col[0]
        else:
            res += c
    return res, double

def is_valid(s):
    for i,c in enumerate(s):
        if i>0 and c!='?' and c==s[i-1]:
            return False
    return True

def consecutive_undef(s):
    for i,c in enumerate(s):
        if i>0 and c=='?' and c==s[i-1]:
            return True
    return False

def is_complete(s):
    return not "?" in s

def extreme_undef(s):
    if s[0]=='?' or s[-1]=='?':
        return True
    return False

import sys
n = int(input())
s = input()
if is_complete(s) or not is_valid(s):
    print("No")
    sys.exit()

possible = set()
colors = set(["M","Y","C"])

if consecutive_undef(s):
    print("Yes")
    sys.exit()

if extreme_undef(s):
    print("Yes")
    sys.exit()

s, double = complete_canvas(s)
if double:
    print("Yes")
    sys.exit()
else:
    print("No")
    sys.exit()
