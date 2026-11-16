import sys
sys.setrecursionlimit(10000) # hago n-1 llamadas recursivas para largo n, por default el limit es 1000 creo

def cantidad_de_brochazos(izq,der,altura):
    """

    :param izq: limite izquierdo de la zona a pintar
    :param der: limite derecho de la zona a pintar
    :param altura: altura hasta la cual ya esta pintada la cerca hacia abajo
    :return: cantidad necesaria
    """
    if izq > der:
        return 0  # caso base

    solo_vertical = der - izq + 1  # siempre esta la opcion de solo hacer trazos verticales
    altura_minima = min(L[izq:der + 1]) #necesitamos saber cual es el bloque con la menor altura
    minimo = izq + L[izq:der + 1].index(altura_minima)

    dividir_y_conquistar = L[minimo] - altura + cantidad_de_brochazos(izq,minimo - 1, L[minimo]) + \
                           cantidad_de_brochazos(minimo + 1, der, L[minimo])

    return min(solo_vertical, dividir_y_conquistar)









if __name__ == '__main__':
    n = int(sys.stdin.readline())
    L = list(map(int, input().split()))
    sys.stdout.write(str(cantidad_de_brochazos(0,n-1,0)))
