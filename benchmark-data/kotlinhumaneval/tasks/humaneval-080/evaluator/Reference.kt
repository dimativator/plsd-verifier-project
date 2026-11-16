fun startsOneEnds(n: Int): Int {
    if (n == 1) {
        return 1
    }
    var answer = 18
    repeat(n - 2) {
        answer *= 10
    }
    return answer
}

