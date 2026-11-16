string = input().split()
first = string[0]
second = string[1]
third = string[2]
string.sort(key=lambda x: int(x[0]))
if first == second == third or first[1] == second[1] == third[1] and all(int(string[i][0]) == int(string[i - 1][0]) + 1 for i in range(1, 3)):
    print(0)
elif (first == second or second == third or third == first or (string[0][1] == string[1][1] and int(string[1][0]) - int(string[0][0]) <= 2) or
        (string[1][1] == string[2][1] and int(string[2][0]) - int(string[1][0]) <= 2) or (string[0][1] == string[2][1] and int(string[2][0]) - int(string[0][0]) <= 2)):
    print(1)
else:
    print(2)