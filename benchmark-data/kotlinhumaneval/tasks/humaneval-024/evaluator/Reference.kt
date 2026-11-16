fun largestDivisor(n: Int): Int {
    for (i in 2..n) {
        if (i * i > n) {
            break
        }
        if (n % i == 0) {
            return n / i
        }
    }
    return 1
}

