n = int(input())
i = 0
s = ''.join(['W' if (i + j) % 2 == 0 else 'B' for i in range(n) for j in range(n)])



while(i<n*n):
    print(s[i:i+n])
    i+=n