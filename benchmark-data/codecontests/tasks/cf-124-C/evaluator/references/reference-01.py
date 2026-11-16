import sys
import math
from collections import defaultdict

MAXNUM = math.inf
MINNUM = -1 * math.inf
ASCIILOWER = 97
ASCIIUPPER = 65


def getInt():
    return int(sys.stdin.readline().rstrip())


def getInts():
    return map(int, sys.stdin.readline().rstrip().split(" "))


def getString():
    return sys.stdin.readline().rstrip()


def printOutput(ans):
    sys.stdout.write()
    pass


def getPrimes(s):
    primes = [2]
    MAX = s + 1
    for i in range(3, MAX):
        STOP = math.ceil(math.sqrt(i) + 1)
        isPrime = True
        for j in range(2, STOP):
            if i % j == 0:
                isPrime = False
        if isPrime:
            primes.append(i)
    return primes


def solve(let, s):
    primes = getPrimes(len(s))
    bigindices = []
    oneIndices = []
    ones = 0

    for i in primes:
        k = len(s) // i
        if k > 1:
            bigindices.append(i)
        if k == 1:
            oneIndices.append(i)
            ones += 1

    solution = [0 for _ in range(len(s))]

    bigK = max(let, key=lambda x: let[x])
    total = 0

    for index in bigindices:
        for i in range(index, len(solution) + 1, index):
            if solution[i-1] == 0:
                solution[i - 1] = bigK
                total += 1

    #print(len(s))
    #print(total)
    #print(bigindices)
    #print(oneIndices)
            
    if total > let[bigK]:
        return "NO", None
    else:
        let[bigK] -= total

    #print("afterbig")
    #print(solution)

    for item in oneIndices:
        for key, val in let.items():
            if val >= 1:
                let[key] -= 1
                ones -= 1
                solution[item - 1] = key
                break

    if ones != 0:
        return "NO", None

    #print("afteroneind")
    #print(solution)

    for i in range(len(solution)):
        if solution[i] == 0:
            for key, val in let.items():
                if val > 0:
                    val -= 1
                    solution[i] = key
                    break
    return "YES", "".join(solution)


def readinput():
    lettercount = defaultdict(int)
    string = getString()
    for ele in string:
        lettercount[ele] += 1
    ans = solve(lettercount, string)
    print(ans[0])
    if ans[0] != "NO":
        print(ans[1])


readinput()
