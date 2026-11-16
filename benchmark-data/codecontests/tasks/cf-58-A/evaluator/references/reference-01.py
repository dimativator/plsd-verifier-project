s=input()

s=s.lower()

ss='hello'
cnt=0
for i in range(len(s)):
  if s[i]==ss[cnt]:
    cnt+=1
  if cnt==5:
    break

if cnt==5:
  print("YES")
else:
  print("NO")
