fun fib(n: Int): Int {
    val fibs = mutableListOf(0, 1)
    while (fibs.size <= n) {
        fibs.add(fibs[fibs.size - 2] + fibs[fibs.size - 1])
    }
    return fibs[n]
}

