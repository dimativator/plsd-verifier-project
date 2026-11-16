n = int(input())
s = input()
s = set(s)
if n<27:
    print(n - len(s))
else:
    print('-1')