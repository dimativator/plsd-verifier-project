n =  int(input())

genom = dict()
heads = set()

for i in range(n):
    part = input()
    heads.add(part[0])
    for i in range(len(part)):
        prev = None
        next = None
        if i - 1 >= 0:
            prev = part[i - 1]
        if i + 1 < len(part):
            next = part[i + 1]

        if part[i] in genom:
            if not genom[part[i]][0]:
                genom[part[i]][0] = prev
            if not genom[part[i]][1]:
                genom[part[i]][1] = next
        else:
            genom[part[i]] = [prev, next]

new_heads = set()

for head in heads:
    if not genom[head][0]:
        new_heads.add(head)

res = ''
for head in new_heads:
    el = head
    while el:
        res += el
        el = genom[el][1]

print(res)

        
