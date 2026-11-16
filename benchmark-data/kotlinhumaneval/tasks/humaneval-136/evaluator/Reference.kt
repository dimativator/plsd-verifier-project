fun specialFactorial(n : Long) : Long {
    fun factorial(n: Long): Long {
        return if (n <= 1) 1 else n * factorial(n - 1)
    }
    var result = 1L
    for (i in 1..n) {
        result *= factorial(i)
    }
    return result
}

