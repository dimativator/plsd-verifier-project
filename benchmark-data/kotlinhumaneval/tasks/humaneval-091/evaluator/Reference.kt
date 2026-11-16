fun skjkasdkd(lst: List<Int>): Int {
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

    var maxPrime = lst.filter { isPrime(it) }.max()
    var digitSum = 0
    while (maxPrime > 0) {
        digitSum += maxPrime % 10
        maxPrime /= 10
    }
    return digitSum
}

