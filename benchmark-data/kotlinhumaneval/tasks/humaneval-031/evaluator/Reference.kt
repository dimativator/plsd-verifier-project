fun isPrime(n: Int): Boolean {
    if (n == 1) {
        return false
    }
    for (i in 2..n) {
        if (i * i > n) {
            break
        }
        if (n % i == 0) {
            return false
        }
    }
    return true
}

