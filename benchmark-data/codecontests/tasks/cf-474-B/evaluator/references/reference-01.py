from bisect import bisect_left

n = int(input())
n1 = input().split()
m = int(input())
m1 = input().split()
lista = []
valor = 0

for e in n1:
    valor += int(e)
    lista.append(valor)

for e in m1:
    print(bisect_left(lista, int(e)) + 1)