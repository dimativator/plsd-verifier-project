import sys as _sys


def main():
    t = int(input())
    for i_t in range(t):
        n, k = _read_ints()
        a = tuple(_read_ints())
        try:
            result = find_min_m(a, k)
        except ValueError:
            result = -1
        print(result)


def _read_line():
    result = _sys.stdin.readline()
    assert result[-1] == "\n"
    return result[:-1]


def _read_ints():
    return map(int, _read_line().split(" "))


def find_min_m(a_seq, k):
    assert k >= 1
    a_seq = tuple(a_seq)
    if a_seq.count(0) == len(a_seq):
        return 0
    steps_n = sum(x1 != x2 for x1, x2 in zip(a_seq, a_seq[1:]))
    
    if k == 1:
        if steps_n == 0:
            return 1
        else:
            raise ValueError("can't find min m")
    
    result = 0
    steps_per_b_seq = k - 1
    if a_seq[0] != 0:
        steps_n += 1
        if steps_n <= k:
            return 1
        steps_n -= k
        result += 1
    result += _ceil_div(steps_n, steps_per_b_seq)
    return result


def _ceil_div(x, y):
    assert y > 0
    result = x // y
    if x % y != 0:
        result += 1
    return result


if __name__ == '__main__':
    main()
