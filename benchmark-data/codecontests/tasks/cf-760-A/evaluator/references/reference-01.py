def read_input():
    line = input().strip().split()
    m = int(line[0])
    week = int(line[1])
    days31 = {1,3,5,7,8,10,12}
    if m == 2:
        days = 28
    elif m in days31:
        days = 31
    else:
        days = 30
    z = (days + week - 1)
    return z//7 if z % 7 == 0 else z//7 + 1

if __name__ == "__main__":
    print(read_input())