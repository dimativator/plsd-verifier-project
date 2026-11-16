n, k = map(int, raw_input().split())
s = raw_input()
g = int(raw_input())
games = [raw_input() for i in range(g)]

MOD_1 = 1000000007
BASE_1 = 31

MOD_2 = 1000000409
BASE_2 = 29

hashes_1 = []
hashes_2 = []
hash_inv = {}
game_inv = {}
for i, game in enumerate(games):
    h_1 = 0
    h_2 = 0
    for c in game:
        h_1 *= BASE_1
        h_2 *= BASE_2
        h_1 += ord(c) - ord('a')
        h_2 += ord(c) - ord('a')
        h_1 %= MOD_1
        h_2 %= MOD_2
    hashes_1.append(h_1)
    hashes_2.append(h_2)
    hash_inv[(h_1, h_2)] = i
    game_inv[game] = i

# assert len(hash_inv) == g
# compute rolling hash on cd string
# find all residues (mod k) at which each game appears

s = s + s
h_1 = 0
h_2 = 0
for i in range(k):
    h_1 *= BASE_1
    h_2 *= BASE_2
    h_1 += ord(s[i]) - ord('a')
    h_2 += ord(s[i]) - ord('a')
    h_1 %= MOD_1
    h_2 %= MOD_2

coef_1 = pow(BASE_1, k - 1, MOD_1)
coef_2 = pow(BASE_2, k - 1, MOD_2)
residues = [set() for i in range(g)]
for i in range(k, len(s)):
    # first, consider the word at [i - k, i)
    # (h = hash of that word)
    if (h_1, h_2) in hash_inv:
        residues[hash_inv[(h_1, h_2)]].add(i % k)
    # update h for next word
    h_1 -= coef_1 * (ord(s[i - k]) - ord('a'))
    h_2 -= coef_2 * (ord(s[i - k]) - ord('a'))
    h_1 *= BASE_1
    h_2 *= BASE_2
    h_1 += ord(s[i]) - ord('a')
    h_2 += ord(s[i]) - ord('a')
    h_1 %= MOD_1
    h_2 %= MOD_2

res_freq = [0]*k
for i in range(g):
    for res in residues[i]:
        res_freq[res] += 1

use = -1
for i in range(k):
    # if s.startswith("muytqaevcsnqpkfxq"):
    #     print i, res_freq[i], n
    if res_freq[i] >= n:
        use = i
        break

if use == -1:
    print "NO"
else:
    print "YES"
    ans = []
    for i in range(n):
        idx = k*i + use
        ss = s[idx:idx+k]
        ans.append(game_inv[ss] + 1)
    print " ".join(map(str, ans))
