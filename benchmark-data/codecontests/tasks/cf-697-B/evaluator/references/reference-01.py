from functools import reduce
import math
from decimal import *
def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
def sol():
    a = Decimal(input())
    if (int(a) == a):
        print(int(a))
    else:
        print(a)

sol()
