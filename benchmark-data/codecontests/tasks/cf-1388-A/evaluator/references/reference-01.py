# import sys

# sys.stdin = open('input.txt', 'r')
# sys.stdout = open('output.txt', 'w')

t = 1
t = int(input())

while t:
    t -= 1

    n = int(input())
    # s = input()
    if n > 30:
        if (n-30) in [6, 10, 14]:
            if n > 31:
                print('YES')
                print(6,10,15,n-31)
            else:
                print('NO')
        else:
            print('YES')
            print(6,10,14,n-30)
    else:
        print('NO')