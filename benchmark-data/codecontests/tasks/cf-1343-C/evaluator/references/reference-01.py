t = int(input())

for tt in range(t):

    n = int(input())
    arr = list(map(int,input().split()))

    mx = arr[0]
    sm = 0

    for j in range(n):

        if (arr[j] * mx  < 0 ):

            sm += mx
            mx = arr[j]

        else:

            mx = max(mx , arr[j])


    print(sm + mx)

