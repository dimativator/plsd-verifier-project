fun maximum(arr : List<Int>, k : Int) : List<Any> {
	return arr.sorted().takeLast(k)
}

