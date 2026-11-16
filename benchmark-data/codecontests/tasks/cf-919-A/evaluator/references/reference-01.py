pointer = 0 
lst = [0, 0]
n, m = list(map(int, input().split()))
for i in range(n):
    a, b = list(map(int, input().split()))
    if (pointer == 0):
        lst[0], lst[1] = a, b
    pointer+=1
    if ((m*lst[0])/lst[1]) > ((m*a)/b):
        lst[0], lst[1] = a, b
print((m*lst[0])/lst[1])