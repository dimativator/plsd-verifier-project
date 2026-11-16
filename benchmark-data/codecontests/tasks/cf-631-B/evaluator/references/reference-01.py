def main():
    n, m, k = map(int, input().split())
    lst = [[0] * m for _ in range(n)]
    rows = {}
    cols = {}
    for i in range(k):
        q, idx, a = map(int, input().split())
        if q == 1:
            rows[idx - 1] = (a, i)
        else:
            cols[idx - 1] = (a, i)

    for r in range(n):
        for c in range(m):
            if r in rows and c in cols:
                if rows[r][1] > cols[c][1]:
                    lst[r][c] = rows[r][0]
                else:
                    lst[r][c] = cols[c][0]
            elif r in rows and c not in cols:
                lst[r][c] = rows[r][0]
            elif r not in rows and c in cols:
                lst[r][c] = cols[c][0]

    for e in lst:
        print(*e)
                
                

if __name__ == '__main__':
    main()
