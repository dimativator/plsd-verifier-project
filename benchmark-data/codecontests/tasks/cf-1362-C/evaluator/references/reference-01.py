class Solution():
    def __init__(self):
        for t in range(int(input())):
            n = int(input())
            self.solve(n)
    
    def solve(self, n):
        b = format(n, "b")
        res = 0
        while b:
            res += int(b, 2)
            b = b[:-1]
        print(res)

Solution()
