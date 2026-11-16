fun generateIntegers(a : Int, b : Int) : List<Int> {
	val l = Math.min(a, b)
    val r = Math.max(a, b)
    return (0..8).filter { it % 2 == 0 && l <= it && it <= r }
}

