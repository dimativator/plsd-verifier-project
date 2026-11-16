import sys
from collections import Counter
from math import factorial

input = sys.stdin
output = sys.stdout

# input = open('input.txt')


def read_int():
    return [int(x) for x in input.readline().rstrip().split()]

line = input.readline().rstrip()
x = ord(line[0]) - ord('a')
y = ord(line[1]) - ord('1')
answer = 0
for _x in range(x - 1, x + 2):
    for _y in range(y - 1, y + 2):
        if _x != x or _y != y:
            if 0 <= _x < 8 and 0 <= _y < 8:
                answer += 1

output.write('%d\n' % answer)
