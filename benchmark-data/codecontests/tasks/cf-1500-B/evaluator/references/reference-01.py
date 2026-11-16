def main():
    n, m, k = list(map(lambda x: int(x), str(input()).split(' ')))
    a = list(map(lambda x: int(x), str(input()).split(' ')))
    b = list(map(lambda x: int(x), str(input()).split(' ')))
    if n < m:
        print(solve(m, n, k, b, a))
        return
    print(solve(n, m, k, a, b))

def solve(n, m, k, a, b):
    # n >= m
    d = gcd(n, m)

    x, y = 0, 0
    # x * n - y * m = d
    for i in range(1, m):
        if (i * n - d) % m == 0:
            x = i
            y = (i * n - d) // m
            if y == 0:
                x += 1
                y += 1
            break
    # print(x, y, d)
    common = {}
    common_count = 0
    colors = {}
    for i in range(len(a)):
        colors[a[i]] = i
    
    for i in range(len(b)):
        if b[i] in colors and (colors[b[i]] - i) % d == 0:
            common[colors[b[i]]] = i
            common_count += 1

    # where the common indices meet
    com = []
    
    for key, val in common.items():
        z = (val - key) // d
        # z * x * n - z * y * m = v - k
        com.append(int(((z * x) % (m // d)) * n + key))
    
    new_k = k % (m * n // d - common_count)
    s = (k // (m * n // d - common_count)) * m * n // d
    if new_k == 0:
        new_k = m * n // d - common_count
        s -= m * n // d


    com = sorted(com)
    cur = -1

    # print(com, s, new_k, common_count, m * n // d - common_count)
    for c in com:
        if new_k < c - cur:
            s += new_k
            return s
        new_k -= (c - cur - 1)
        s += (c - cur)
        cur = c
    return s + new_k

def gcd(n, m):
    if n == m:
        return n
    if n < m:
        return gcd(m, n)
    if n % m == 0:
        return m
    return gcd(m, n % m)

if __name__ == "__main__":
    main()