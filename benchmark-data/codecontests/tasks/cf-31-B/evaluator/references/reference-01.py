def main():
    string = input()
    comps = string.split('@')
    ans = []
    if '@' not in string:
        print("No solution")
        return
    for i in range(len(comps)):
        if i == 0 or i == len(comps) - 1:
            if len(comps[i]) < 1:
                print("No solution")
                return 
        else:
            if len(comps[i]) < 2:
                print("No solution")
                return 
    if len(comps) == 2:
        print('@'.join(comps))
        return 
    for i in range(len(comps) - 1):
        if i == 0:
            ans.append(comps[i] + '@' + comps[i + 1][:1])
        elif i == len(comps) - 2:
            ans.append(comps[i][1:] + '@' + comps[i + 1])
        else:
            ans.append(comps[i][1:] + '@' + comps[i + 1][:1])
    print(','.join(ans))

main()
