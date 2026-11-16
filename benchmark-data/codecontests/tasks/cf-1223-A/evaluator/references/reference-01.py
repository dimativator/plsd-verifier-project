# import numpy as np


import array


def solution():
    req = int(input())
    for i in range(req):
        count = int(input())
        result = 0
        if count==2:
            print(2)
            continue
        while count % 2 != 0 :
            result+=1
            count+=1
        print(result)



def count_of_one(number):
    result = 0
    while number:
        result += number % 2
        number //= 2
    return result


def to_mixed_frac(first, second):
    while True:
        for i in range(2, first + 1):
            if first % i == 0 and second % i == 0:
                first //= i
                second //= i
                break
        else:
            break
    return str(first) + "/" + str(second)


def array_to_int(array):
    for i in range(len(array)):
        array[i] = int(array[i])
    return array


def join0(array):
    result = ""
    for i in array:
        result += str(i)
    return result


def replace(string, new_ch, index):
    new_str = ""
    for i in range(len(string)):
        if i == index:
            new_str += new_ch
        else:
            new_str += string[i]
    return new_str


solution()
# input-output by console
