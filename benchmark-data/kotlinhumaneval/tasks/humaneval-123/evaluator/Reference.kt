fun isSorted(lst : List<Int>) : Boolean {
	val diffs = lst.zipWithNext { a, b -> b - a }
    return diffs.all { it >= 0 } && diffs.zipWithNext().all { (a, b) -> a + b > 0 }
}

