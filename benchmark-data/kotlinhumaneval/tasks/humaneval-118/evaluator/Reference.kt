fun solution(lst : List<Int>) : Int {
	return lst.filterIndexed { index, i ->
        index % 2 == 0 && i % 2 == 1
    }.sum()
}

