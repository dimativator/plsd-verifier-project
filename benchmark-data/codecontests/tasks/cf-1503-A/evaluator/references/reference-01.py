T = int(input())
for ts in range(T):
    N = int(input())
    s = input()
    if s[0] == '0' or s[-1] == '0':
        print("NO")
        continue
    a = ['(']
    b = ['(']
    # y_n = 0
    # y = jie(1, 1, 1)
    # if y == 1:
    #     print("YES")
    #     print(''.join(a))
    #     print(''.join(b))
    # else:
    #     print("NO")
    ca = 1
    cb = 1
    for i in range(1, N-1):
        if s[i] == '1':
            if ca == 0 or cb == 0:
                a.append('(')
                b.append('(')
                ca += 1
                cb += 1
            elif ca == cb == 1:
                if s[i+1] == '1':
                    a.append(')')
                    b.append(')')
                    ca -= 1
                    cb -= 1
                else:
                    a.append('(')
                    b.append('(')
                    ca += 1
                    cb += 1
            else:
                a.append(')')
                b.append(')')
                ca -= 1
                cb -= 1
        else:
            if ca == 0:
                a.append('(')
                b.append(')')
                ca += 1
                cb -= 1
            elif cb == 0:
                a.append(')')
                b.append('(')
                ca -= 1
                cb += 1
            elif ca > cb:
                a.append(')')
                b.append('(')
                ca -= 1
                cb += 1
            else:
                a.append('(')
                b.append(')')
                ca += 1
                cb -= 1
    a.append(')')
    b.append(')')
    ca -= 1
    cb -= 1
    if ca == cb == 0:
        print("YES")
        print(''.join(a))
        print(''.join(b))
    else:
        print("NO")