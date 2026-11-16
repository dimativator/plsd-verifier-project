from operator import add
import sys
from array import array  # noqa: F401
from typing import TypeVar, Generic, Callable, List
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


def input():
    return sys.stdin.buffer.readline().decode('utf-8')


n = int(input())
a = [tuple(map(int, input().split())) for _ in range(n)]
max_n = 10**6 + 10
imos = [0] * max_n
for l, r in a:
    imos[l] += 1
    imos[r] -= 1

for i in range(max_n - 5):
    imos[i + 1] += imos[i]

segt = SegmentTree[int](max_n, 0, max, add)
segt.build(imos)

ans = []

for i, (l, r) in enumerate(a, start=1):
    if segt.find(0, l) <= 1 and segt.find(l, r) <= 2 and segt.find(r, max_n) <= 1:
        ans.append(i)

print(len(ans))
print(*ans)
