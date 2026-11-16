from collections import Counter
s = input()
counter = Counter()
for i in range(len(s)):
    counter[s[i:len(s)] + s[0:i]] = 1
print(sum(counter.values()))