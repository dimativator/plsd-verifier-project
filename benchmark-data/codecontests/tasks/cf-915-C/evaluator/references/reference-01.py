import copy
Num1, Num2 = sorted(list(input())), list(input())
Num1.reverse()
Temp1, Temp2, i, j, Result= copy.copy(Num1), copy.copy(Num2), 0, 0, []

if len(Temp1) < len(Temp2):
    print(''.join(Temp1))
    exit()

while True:
    if i + 1 > len(Temp1):
        Temp1.append(Result[len(Result) - 1])
        Temp1.sort()
        Temp1.reverse()
        i = Temp1.index(Result[len(Result) - 1]) + Temp1.count(Result[len(Result) - 1])
        del Result[len(Result) - 1]
        j -= 1
    elif i + 1 == len(Temp1):
        if Temp1[i] < Temp2[j]:
            print(''.join(Result) + Temp1[i] + ''.join(Temp1[:i] ))
            exit()
        elif Temp1[i] == Temp2[j]:
            if j == len(Temp2) - 1:
                print(''.join(Result) + Temp1[i])
                exit()
            elif j == 0:
                Start = i;
            Result.append(Temp1[i])
            del Temp1[i]
            i, j = 0, j + 1
        else:
            Temp1.append(Result[len(Result) - 1])
            Temp1.sort()
            Temp1.reverse()
            i = Temp1.index(Result[len(Result) - 1]) + Temp1.count(Result[len(Result) - 1])
            del Result[len(Result) - 1]
            j -= 1
    else:
        if Temp1[i] < Temp2[j]:
            print(''.join(Result) + Temp1[i] + ''.join(Temp1[:i] + Temp1[i + 1:]))
            exit()
        elif Temp1[i] == Temp2[j]:
            if j == 0:
                Start = i;
            Result.append(Temp1[i])
            del Temp1[i]
            i, j = 0, j + 1
        elif Temp1[i] > Temp2[j]:
            i += 1
