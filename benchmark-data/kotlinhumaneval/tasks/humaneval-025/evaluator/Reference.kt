fun factorize(n: Int): List<Int> {
    var curN = n
    val factors = mutableListOf<Int>()
    for (i in 2..n) {
        if (i * i > n) {
            break
        }
        while (curN % i == 0) {
            curN /= i
            factors.add(i)
        }
    }
    if (curN != 1) {
        factors.add(curN)
    }
    return factors
}

