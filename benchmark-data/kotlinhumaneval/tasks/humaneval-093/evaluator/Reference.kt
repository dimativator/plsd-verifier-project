fun countUpTo(n: Int): List<Any> {
    fun isPrime(num: Int): Boolean {
        if (num == 1) {
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
    return (2 until n).filter { isPrime(it) }
}

