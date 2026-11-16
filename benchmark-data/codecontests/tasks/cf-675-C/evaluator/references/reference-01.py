n = int(input())
b = list(map(int, input().split()))

from collections import Counter
from itertools import accumulate
cum = list(accumulate(b))
cnt = Counter(cum)
print (n - cnt.most_common(1)[0][1])
