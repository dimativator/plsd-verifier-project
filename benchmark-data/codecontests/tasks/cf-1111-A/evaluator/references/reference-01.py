import math

# n=int(input())
s=input()
t=input()
c = ['a','e','i','o','u']
if len(s)!=len(t):
	print("No")
	exit(0)
for i in range(len(s)):
	if(s[i] in c and not(t[i] in c)):
		print("No")
		exit(0)
	elif(t[i] in c and not (s[i] in c)):
		print("No")
		exit(0)
print("Yes")