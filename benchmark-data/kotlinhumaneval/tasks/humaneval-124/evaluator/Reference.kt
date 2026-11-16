fun intersection(interval1 : List<Int>, interval2 : List<Int>) : String {
    fun isPrime(num: Int): Boolean {
        if (num <= 1) {
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
	return if (isPrime(Math.min(interval1[1], interval2[1]) - Math.max(interval1[0], interval2[0]))) {
        "YES"
    } else {
        "NO"
    }
}

