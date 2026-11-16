fun fib4(n: Int): Int {
    val fibs = mutableListOf(0, 0, 2, 0)
    var index = 0
    while (fibs.size <= n) {
        fibs.add(fibs[index] + fibs[index + 1] + fibs[index + 2] + fibs[index + 3])
        index++
    }
    return fibs[n]
}

