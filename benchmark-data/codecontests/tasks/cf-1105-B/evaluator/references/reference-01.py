import bisect

def level(xs, k):
    level = 0
    index = 0
    while index < len(xs):
        level += 1
        index = bisect.bisect_left(xs, xs[index] + k, index)
    return level

"""
assert level([], 2) == 0
assert level([0,1], 2) == 1
assert level([0,1,2], 2) == 2
assert level([10,12,14], 2) == 3
assert level([0,1,12,14], 2) == 3
"""

def all_same(string):
    for i in range(1, len(string)):
        if string[i] != string[i - 1]:
            return False
    return True

"""
assert all_same("")
assert all_same("a")
assert all_same("aa")
assert all_same("aaa")
assert not all_same("baa")
assert not all_same("ba")
"""

def solve(string, k):
    if len(string) < k:
        return 0

    data = {}
    freq = {}
    for c in string[:k]:
        freq[c] = freq.get(c, 0) + 1

    index = 0
    while index <= len(string) - k:
        if index > 0:
            freq[string[index - 1]] -= 1
            freq[string[index + k - 1]] = freq.get(string[index + k - 1], 0) + 1

        if freq[string[index]] == k:
            #print("Found all same chars at", index)
            if string[index] not in data:
                data[string[index]] = []
            data[string[index]].append(index)
    
        index += 1

    max_level = 0
    for char, xs in data.items():
        candidate = level(xs, k)
        if candidate > max_level:
            max_level = candidate
            #print("Found new max of length", candidate, char * k)
    return max_level

n, k = map(int, input().split())
string = input()[:n]
print(solve(string, k))
