fun doubleTheDifference(lst : List<Number>) : Int {
	return lst.sumOf { if (it is Int && it > 0 && it % 2 == 1) it * it else 0 }
}

