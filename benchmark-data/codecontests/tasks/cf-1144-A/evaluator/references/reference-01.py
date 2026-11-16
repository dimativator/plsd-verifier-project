import string

alphabet = string.ascii_lowercase

n = int(input())

for i in range(n):
  s = list(input())
  if len(s) > 26 or len(s) > len(set(s)):
    print("No")
  else:
    s.sort()
    ind = alphabet.index(s[0])
    if alphabet[ind+len(s)-1] == s[-1]:
      print("Yes")
    else:
      print("No")
