from collections import defaultdict
_ =  input()

nums  = list(map(int, input().split()))

freqs = defaultdict(list)

_max =  -1
for i, k in enumerate(nums):
    freqs[k].append(i + 1)
    _max = max(_max, len(freqs[k]))


start = 1
end = len(nums)
length = end - start
for k, v in freqs.items():
    if len(v) == _max:
        if v[-1] - v[0] < length:
            start = v[0]
            end = v[-1]
            length  = end - start

print(start, end)

