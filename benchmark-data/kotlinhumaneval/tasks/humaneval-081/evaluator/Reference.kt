fun solve(n: Int): String {
    var cur = n
    var digitSum = 0
    while (cur > 0) {
        digitSum += cur % 10
        cur /= 10
    }
    return digitSum.toString(2)
}

