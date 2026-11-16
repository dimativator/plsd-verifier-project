fun isMultiplyPrime(a: Int): Boolean {
    var cur = a
    val factors = mutableListOf<Int>()
    for (i in 2..a) {
        if (i * i > a) {
            break
        }
        while (cur % i == 0) {
            cur /= i
            factors.add(i)
        }
    }
    if (cur != 1) {
        factors.add(cur)
    }
    return factors.size == 3
}

