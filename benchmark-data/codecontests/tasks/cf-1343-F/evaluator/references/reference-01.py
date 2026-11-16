for _ in range(int(input())):
    n = int(input())
    segs = [tuple(sorted(int(x) for x in input().split()[1:])) for __ in range(n - 1)]
    segs_having = [[j for j, seg in enumerate(segs) if i in seg] for i in range(n + 1)]
    segs_set = set(segs)
    for first in range(1, n + 1):
        try:
            segs_copy = [set(seg) for seg in segs]
            ans = [first]
            while len(ans) < n:
                for seg in segs_having[ans[-1]]:
                    segs_copy[seg].remove(ans[-1])
                ans.append(next(iter(next(seg for seg in segs_copy if len(seg) == 1))))
            if all(any(tuple(sorted(ans[j:i])) in segs_set for j in range(0, i - 1)) for i in range(2, n + 1)):
                print(*ans)
                break
        except StopIteration:
            pass
