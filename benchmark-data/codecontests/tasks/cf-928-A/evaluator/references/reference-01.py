def f(s):
    return s.lower().replace('1', 'l').replace('0', 'o').replace('i', 'l')

s = f(input())
n = int(input())

l = {f(input()) for _ in range(n)}

print('No' if s in l else 'Yes')
