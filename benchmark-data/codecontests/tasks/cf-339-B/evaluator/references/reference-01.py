def main(n, m, lst):
    count = 0
    lst = [1] + lst
    for i in range(1, len(lst)):
        if lst[i] >= lst[i-1]:
            count += lst[i] - lst[i-1]
        else:
            count += n - lst[i-1] + lst[i]
    return count

n, m = [int(x) for x in input().split()]
lst = list(map(int, input().split()))
print(main(n, m, lst))

