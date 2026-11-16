fun fibfib(n: Int): Int {
    val fibs = mutableListOf(0, 0, 1)
    var index = 0
    while (fibs.size <= n) {
        fibs.add(fibs[index] + fibs[index + 1] + fibs[index + 2])
        index++
    }
    return fibs[n]
}

