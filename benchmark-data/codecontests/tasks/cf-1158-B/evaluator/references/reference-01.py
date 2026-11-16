#  =========     /\       /|    |====/|
#      |        /  \       |    |   / |
#      |       /____\      |    |  /  |
#      |      /      \     |    | /   |
#  ========= /        \  =====  |/====|  
#  code

if __name__ == "__main__":
    n,k = map(int,input().split())
    a = (n - k)//2
    ps = '0'*a + '1'
    s = ""
    i = 0
    while i + a + 1 <= n:
        s += ps
        i += a+1
    if i < n:
        x = n - i
        s += ps[:x]
    print(s)

