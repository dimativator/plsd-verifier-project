from collections import Counter


def main():
    n, m = map(int, input().split())

    c = list(map(int, input().split()))

    sc = sorted(range(n), key=lambda x: c[x])
    mc = Counter(c).most_common(1)[0][1]

    print(n if mc <= n - mc else 2*(n - mc))
    
    for i in range(n):
        print(c[sc[i]], c[sc[i-mc]])


if __name__ == '__main__':
    main()





# Made By Mostafa_Khaled