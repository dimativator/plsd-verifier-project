def inp():
    return [int(s) for s in input().split()]


if __name__ == '__main__':
    for i in range(int(input())):
        s = input()
        output = ''
        if len(s) == 1 and s[0] == '?':
            s = 'a'

        for j in range(len(s)):
            if s[j] != '?':
                output += s[j]
                continue

            av = ['a', 'b', 'c', '?', '?']
            if j == 0:
                av.remove(s[j + 1])
                output += av[0]
            elif j == (len(s) - 1):
                av.remove(output[j - 1])
                output += av[0]
            else:
                av.remove(s[j + 1])
                if output[j - 1] in av:
                    av.remove(output[j - 1])
                output += av[0]

        flag = True
        for j in range(1, len(output)):
            if output[j - 1] == output[j]:
                flag = False
                break
        if flag:
            print(output)
        else:
            print(-1)
