fun sumSquares(lst : List<Double>) : Int {
	return lst.map { Math.ceil(it).toInt() }.sumOf { it * it }
}

