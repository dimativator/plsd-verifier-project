fun isSimplePower(x: Int, n: Int): Boolean {
    var cur = x
    while (cur > 1 && n > 1 && cur % n == 0) {
        cur /= n
    }
    return cur == 1
}

