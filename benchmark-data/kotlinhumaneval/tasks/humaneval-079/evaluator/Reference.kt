fun primeLength(string: String): Boolean {
    fun isPrime(num: Int): Boolean {
        if (num == 1 || num == 0) {
            return false
        }
        for (i in 2..num) {
            if (i * i > num) {
                break
            }
            if (num % i == 0) {
                return false
            }
        }
        return true
    }
    return isPrime(string.length)
}

