t = int(input())
setups = []
for _ in range(t):
    n = int(input())
    setup = []
    for _ in range(n):
        count_and_list = input().split(" ")
        if len(count_and_list) == 1:
            husbands = tuple()
        else:
            husbands = tuple(int(x) for x in count_and_list[1:])
        setup.append(husbands)
    setups.append(setup)

def process(setup):
    available_husbands = set(range(1, len(setup)+1))
    for daughter_index, daughter_prefs in enumerate(setup, 1):
        took_someone = False
        for husband in daughter_prefs:
            if husband in available_husbands:
                took_someone = True
                available_husbands.remove(husband)
                break
        if not took_someone:
            bad_daughter = daughter_index
    if len(available_husbands) > 0:
        print("IMPROVE")
        print(f"{bad_daughter} {available_husbands.pop()}")
    else:
        print("OPTIMAL")


for setup in setups:
    process(setup)
