
def PolandBall(n, k):
    # condiciones que no cumplen con los requisitos
    if n < 4 or k > 3 or k == 1 or (k == 2 and n == 4):
        print('-1')
        return

    # si k=2
    if k == 2:
        print(n-1)
        for i in range(1, n):
            print(str(i)+' '+str(i+1))
        return

    # si k=3 y n=4
    if n == 4:
        print(n-1)
        print('1 2')
        print('2 3')
        print('3 4')
        return

     # si k=3 y n>4
    print(n)
    print('1 2')
    print('2 3')
    print('1 4')
    print('3 5')
    for i in range(5, n+1):
        print('1 '+str(i))


n, k = map(int, input().split())
PolandBall(n, k)

# Casos de prueba:
# 4 1  ##respuesta -1
# 5 2  ##respuesta  4

# 2 1        ##respuesta -1
# 2 3        ##respuesta -1
# 3 3        ##respuesta -1

# 4 2        ##respuesta -1
# 7 2        ##respuesta 6
# 100 2      ##respuesta 99
# 500 2      ##respuesta 499
# 1000 2     ##respuesta 999

# 4 3        ##respuesta 3
# 7 3        ##respuesta 7
# 100 3      ##respuesta 100
# 500 3      ##respuesta 500
# 1000 3     ##respuesta 1000

# 1000 1000  ##respuesta -1
