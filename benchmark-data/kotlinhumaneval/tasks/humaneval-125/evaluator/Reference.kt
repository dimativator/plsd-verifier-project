fun prodSigns(arr : List<Int>) : Int? {
    if (arr.size == 0) {
        return null
    }
	return arr.sumOf { Math.abs(it) } * if (0 in arr) 0 else if (arr.count { it < 0 } % 2 == 1) -1 else 1
}

