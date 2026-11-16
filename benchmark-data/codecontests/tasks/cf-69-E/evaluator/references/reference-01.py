from typing import TypeVar, Generic, Callable, List
import sys
from array import array  # noqa: F401
from collections import Counter


def input():
    return sys.stdin.buffer.readline().decode('utf-8')


minf = -10**9 - 100


T = TypeVar('T')


class SegmentTree(Generic[T]):
    __slots__ = ["size", "tree", "identity", "op", "update_op"]

    def __init__(self, size: int, identity: T, op: Callable[[T, T], T],
                 update_op: Callable[[T, T], T]) -> None:
        self.size = size
        self.tree = [identity] * (size * 2)
        self.identity = identity
        self.op = op
        self.update_op = update_op

    def build(self, a: List[T]) -> None:
        tree = self.tree
        tree[self.size:self.size + len(a)] = a

        for i in range(self.size - 1, 0, -1):
            tree[i] = self.op(tree[i << 1], tree[(i << 1) + 1])

    def find(self, left: int, right: int) -> T:
        left += self.size
        right += self.size
        tree, result, op = self.tree, self.identity, self.op

        while left < right:
            if left & 1:
                result = op(tree[left], result)
                left += 1
            if right & 1:
                result = op(tree[right - 1], result)
            left, right = left >> 1, right >> 1

        return result

    def update(self, i: int, value: T) -> None:
        op, tree = self.op, self.tree
        i = self.size + i
        tree[i] = self.update_op(tree[i], value)

        while i > 1:
            i >>= 1
            tree[i] = op(tree[i << 1], tree[(i << 1) + 1])


n, k = map(int, input().split())
a = [int(input()) for _ in range(n)]
ans = ['Nothing'] * (n - k + 1)

comp_dict = {x: i for i, x in enumerate(sorted(set(a)), start=1)}
m = len(comp_dict) + 10
rmq = SegmentTree[int](m, minf, max, lambda x, y: y)
cnt = Counter()

for i in range(k):
    cnt[a[i]] += 1
for key, val in cnt.items():
    if val == 1:
        rmq.update(comp_dict[key], key)

res = rmq.find(0, m)
if res != minf:
    ans[0] = str(res)

for i in range(k, n):
    cnt[a[i]] += 1
    cnt[a[i - k]] -= 1
    if a[i] != a[i - k]:
        if cnt[a[i]] == 1:
            rmq.update(comp_dict[a[i]], a[i])
        elif cnt[a[i]] == 2:
            rmq.update(comp_dict[a[i]], minf)
        if cnt[a[i - k]] == 1:
            rmq.update(comp_dict[a[i - k]], a[i - k])
        elif cnt[a[i - k]] == 0:
            rmq.update(comp_dict[a[i - k]], minf)

    res = rmq.find(0, m)
    if res != minf:
        ans[i - k + 1] = str(res)

sys.stdout.buffer.write('\n'.join(ans).encode('utf-8'))
