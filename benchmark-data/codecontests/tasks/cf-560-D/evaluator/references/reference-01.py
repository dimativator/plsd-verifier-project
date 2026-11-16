def equals(a, b):
  if (a == b):
    return True
  
  len_a, len_b = len(a), len(b)

  if (len_a & 1 or len_b & 1):
    return False
  
  if (len_a == 1):
    return False

  as1 = a[0:len_a//2]
  as2 = a[len_a//2:(len_a//2)*2]
  bs1 = b[:len_b//2]
  bs2 = b[len_b//2:(len_b//2)*2]

  return (equals(as1, bs2) and equals(as2, bs1)) or (equals(as1, bs1) and equals(as2, bs2))

s1 = input()
s2 = input()

if (equals(s1, s2)):
  print("YES")
else:
  print("NO")