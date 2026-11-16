n, m = (int(x) for x in input().split())
happy_boys = [0 for _ in range(n)]
happy_girls = [0 for _ in range(m)]
boys = [int(x) for x in input().split()]
girls = [int(x) for x in input().split()]
if boys[0]:
    for i in range(1, len(boys)):
        happy_boys[boys[i]] = 1

if girls[0]:
    for i in range(1, len(girls)):
        happy_girls[girls[i]] = 1
# print (happy_boys)
# print (happy_girls)
add_val = max(n, m)
days_left = m * n + 1
cur_day = 0
while cur_day < days_left:
    if happy_boys[cur_day % n] ^ happy_girls[cur_day % m]:
        days_left += add_val
        # print(happy_boys)
        # print(happy_girls)
        # print("")
        happy_boys[cur_day % n] = happy_girls[cur_day % m] = 1
        # print(happy_boys)
        # print(happy_girls)
    cur_day += 1
if all(happy_boys) and all(happy_girls):
    print("Yes")
else:
    print("No")
