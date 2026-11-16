rever = "AHIMOTUVWXYovwx"
rev = ["bd", "pq","db","qp"]
line = input().rstrip()
if len(line) & 1 and line[len(line) // 2] not in rever:
    print("NIE")
    exit()

l = len(line) // 2 - 1
r = len(line) // 2 if len(line) & 1 == 0 else\
    len(line) // 2 + 1

for i in range(len(line) // 2):
    if line[l] + line[r] not in rev and (line[l] not in rever or line[l] != line[r]):
        break
    l-=1
    r+=1
if l != -1 or r != len(line):
    print("NIE")
else:
    print("TAK")