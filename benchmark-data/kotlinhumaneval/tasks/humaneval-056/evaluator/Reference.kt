fun largestPrimeFactor(n: Int): Int {
    var curN = n
    var maxFactor = 1
    for (i in 2..n) {
        if (i * i > n) {
            break
        }
        while (curN % i == 0) {
            curN /= i
            maxFactor = i
        }
    }
    if (curN > maxFactor) {
        maxFactor = curN
    }
    return maxFactor
}

