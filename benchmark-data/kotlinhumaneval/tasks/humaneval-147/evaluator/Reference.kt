fun xOrY(n : Int, x : Int, y : Int) : Int {
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
    return if (isPrime(n)) {
        x
    } else {
        y
    }
}

