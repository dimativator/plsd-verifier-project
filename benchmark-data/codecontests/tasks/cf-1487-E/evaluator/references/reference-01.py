MAX_VAL = 2 ** 31


def prepare_values(vals):
    zipped_vals = list(zip(vals, range(1, len(vals) + 1)))
    zipped_vals.sort()
    pairs = [(old_i, i) for i, (val, old_i) in enumerate(zipped_vals, 1)]
    return zipped_vals, dict(pairs)


def renumber_ids(dic, l):
    return [dic[x] for x in l]


def get_first_absent(l):
    l.sort()
    i = 1
    for x in l:
        if i != x:
            return i
        i += 1

    return i


def read_mismatches():
    n = int(input())
    mismatches = dict()
    for _ in range(n):
        x, y = map(int, input().split())
        l = mismatches.get(x, [])
        l.append(y)
        mismatches[x] = l

    return n, mismatches


def accumulate_cost(to_accumulate, from_accumulate, mismatches):
    n = len(to_accumulate)

    from_zipped, from_dic = prepare_values(from_accumulate)

    for x in range(1, n + 1):
        l = mismatches.get(x, [])
        renumbered_l = renumber_ids(from_dic, l)
        first_absent = get_first_absent(renumbered_l)

        if first_absent > len(from_accumulate):
            to_accumulate[x - 1] = MAX_VAL
        else:
            to_accumulate[x - 1] += from_zipped[first_absent - 1][0]

    return 0


def solution():
    n1, n2, n3, n4 = map(int, input().split())

    first_course = list(map(int, input().split()))
    second_course = list(map(int, input().split()))
    drink = list(map(int, input().split()))
    dessert = list(map(int, input().split()))

    m1, fc_sc_mismatch = read_mismatches()
    m2, sc_drink_mismatch = read_mismatches()
    m3, drink_dessert_mismatch = read_mismatches()

    # drinks
    accumulate_cost(drink, dessert, drink_dessert_mismatch)

    # second_course
    accumulate_cost(second_course, drink, sc_drink_mismatch)

    # first course
    accumulate_cost(first_course, second_course, fc_sc_mismatch)

    result = min(first_course)
    print(-1 if result >= MAX_VAL else result)
    
solution()