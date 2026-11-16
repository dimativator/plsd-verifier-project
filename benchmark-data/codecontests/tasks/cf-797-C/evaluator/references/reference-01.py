


s = list(input())
t = []
u = []

letters = [[] for _ in range(ord('z') - ord('a') + 1)]

for (index, letter) in enumerate(s):
    letters[ord(letter) - ord('a')] += [index]

for indexes in letters:
    indexes.reverse()

current = 0
while current < len(s):
    if len(t) == 0:
        t += s[current]
        letters[ord(s[current]) - ord('a')].pop()
        current += 1
        continue

    best_in_word = chr(ord('z') + 1)
    best_index = -1
    for i in range(ord('z') - ord('a') + 1):
        if len(letters[i]) != 0:
            best_in_word = chr(ord('a') + i)
            best_index = letters[i][-1]
            break

    if t[-1] <= best_in_word:
        u += t[-1]
        t.pop()
        continue

    while current <= best_index:
        t += s[current]
        letters[ord(s[current]) - ord('a')].pop()
        current += 1

while len(t) > 0:
    u += t[-1]
    t.pop()

print(''.join(u))
