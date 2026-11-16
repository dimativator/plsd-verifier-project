# QAQ
def crying(s):
    ans = 0
    for i in range(len(s)):
        if (s[i] != "Q"):
            continue
        for j in range(i + 1, len(s)):
            if s[j] != 'A':
                continue
            for k in range(j + 1, len(s)):
                if s[k] == 'Q':
                    ans += 1
                            

    return ans




s = input()
print(crying(s))