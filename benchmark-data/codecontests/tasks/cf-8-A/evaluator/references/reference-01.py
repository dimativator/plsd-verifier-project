import re

I = input

s, first, second = I(), I(), I()

forward = re.fullmatch('\w*' + first + '\w*' + second + '\w*', s)
backward = re.fullmatch('\w*' + first + '\w*' + second + '\w*', s[::-1])

if forward:
    print('both' if backward else 'forward')
else:
    print('backward' if backward else 'fantasy')