def main():
    n, m, x, y = map(int, input().split())

    col = [0] * m
    for i in range(n):
        row = input()
        for j in range(m):
            if row[j] == '.':
                col[j] += 1

    acc = [0]
    for j in range(m):
        acc.append(acc[-1] + col[j])

    dp = [[0]*(m+1), [0]*(m+1)]

    for j in range(1, m+1):
        dp[0][j] = float('infinity')
        dp[1][j] = float('infinity')
        for k in range(x, y+1):
            if j-k >= 0:
                wp = acc[j] - acc[j-k]
                bp = k * n - wp
                dp[0][j] = min(dp[0][j], dp[1][j-k] + wp)
                dp[1][j] = min(dp[1][j], dp[0][j-k] + bp)

    print(min(dp[0][m], dp[1][m]))


if __name__ == "__main__":
    main()
