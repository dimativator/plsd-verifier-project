def calculate(n):
    res = 0
    if (n%2 == 1):
        for i in range(2, n+2, 2):
            res += i
        return res * 2
    else:
        if (n%4 == 0):
            for i in range(1, int(n/2) + 1):
                res += i
            res *= 2
            res += n/2 + 1
            return int(res)
        else:
            for i in range(1, int(n/2) + 1):
                res += i
            res *= 2
            
            res += (n+2)/2
            return int(res)
print(calculate(int(input())))