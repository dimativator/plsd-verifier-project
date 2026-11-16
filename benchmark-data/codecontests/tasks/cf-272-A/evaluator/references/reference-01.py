def solve(n,d):
    other = 0
    for i in d:
        other += i
    
    ways = 0
    for i in range(1,6):
        if (other + i) % (n + 1) != 1:
            ways += 1

    print(ways)

def main():
    n = int(input())
    d = input()
    d = [int(i) for i in d.split()]
    solve(n,d)

main()