t = int(input())
def max_subarray(arr):
    max_ending = max_current = arr[0]
    for i in arr[1:]:
        max_ending = max(i, max_ending + i)
        max_current = max(max_current, max_ending)
    return max_current

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))


    if max_subarray(a[1:]) < sum(a) and max_subarray(a[:-1]) < sum(a):
        print("YES")
    else:
        print("NO")
