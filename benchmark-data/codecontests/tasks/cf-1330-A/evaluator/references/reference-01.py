cycles = int(input())

def find_v(x, places):
    places = set(places)
    v = 0
    i = 1
    while True:
        if i in places:
            v = i
        elif x > 0:
            v = i
            x -= 1
        else:
            break
        i += 1
    return v



results = []

for cycle in range(cycles):
    n, x = map(int, input().split())
    places = map(int, input().split())
    results.append(find_v(x, places))

for r in results:
    print(r)
