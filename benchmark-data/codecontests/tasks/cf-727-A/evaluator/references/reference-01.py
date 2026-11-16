n, target = map(int, input().split())


def keep(target, ans):
    #print(target)
    while target % 2 == 0:
        target = target // 2
        ans = [target]+ans
    if str(target).endswith("1") and target != 1:
        return keep((target-1) // 10, [(target-1) // 10]+ans)
    else:
        return target, ans

next, nos = keep(target, [target])

if n in nos:
    print("YES")
    nos = nos[nos.index(n):]
    print(len(nos))
    print(" ".join(str(k) for k in nos))
else:
    print("NO")