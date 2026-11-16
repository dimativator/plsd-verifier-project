fun addElements(arr : List<Int>, k : Int) : Int {
	return arr.take(k).filter { it < 100 }.sum()
}

