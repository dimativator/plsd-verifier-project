from collections import Counter
n = int(input())
print("Yes" if n == 1 or max(Counter(input()).values()) >= 2 else "No")