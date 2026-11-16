n = int(input())
houses = sorted(set(map(int, input().split())))

if len(houses) <= 3:
    print(0)
    result = houses[:]
    while len(result) < 3:
        result.append(result[-1])
    print('%.6f %.6f %.6f' % tuple(result))
    import sys; sys.exit()

span = 0
left = 1
right = len(houses) - 2
#print(houses)
#print('span = %d, houses[%d] = %d, houses[%d] = %d' % (span,
#    left, houses[left], right, houses[right]))

while houses[right] - houses[left] > span:
    left_gap = houses[left] - houses[0] - span
    right_gap = houses[-1] - houses[right] - span
    middle = houses[right] - houses[left]
    if left_gap <= right_gap:
        if span + left_gap > middle:
            span = middle
            break
        left += 1
        if left_gap == right_gap:
            right -= 1
        span += left_gap
    else:
        if span + right_gap > middle:
            span = middle
            break
        right -= 1
        span += right_gap
    #print('span = %d, houses[%d] = %d, houses[%d] = %d' % (span,
    #    left, houses[left], right, houses[right]))

print('%.6f' % (span / 2))
print('%.6f %.6f %.6f' % ((houses[0] + houses[left - 1]) / 2,
                          (houses[left] + houses[right]) / 2,
                          (houses[right + 1] + houses[-1]) / 2))
