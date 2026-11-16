t = int(input())
for i in range(t):
    n, k = map(int, input().split())
    s = input()
    index = s.find('*')
    num = 1
    last = s.rfind('*')
    while index < last:
        if s[index] == '*':
            index += k
            num += 1
        else:
            index -= 1
    print(num)