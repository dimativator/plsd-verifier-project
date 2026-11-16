n = int(input())
s = 'ROYGBIV'
s1 = 'GBIV'
print(s, (n - 7) // 4 * s1, s1[:(n - 7) % 4], sep='')
