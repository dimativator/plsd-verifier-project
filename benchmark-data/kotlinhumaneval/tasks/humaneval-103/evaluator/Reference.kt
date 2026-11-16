fun f(n : Int) : List<Int> {
    fun factorial(num: Int): Int = if (num == 0) 1 else num * factorial(num - 1)
    fun sumToNum(num: Int): Int = (1..num).sum()
    return (1..n).map { i ->
        if (i % 2 == 0) factorial(i) else sumToNum(i)
    }
}

