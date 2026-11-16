fun evenOddCount(num : Int) : List<Int> {
    val digits = num.toString().filter { it.isDigit() }
    val evenCount = digits.count { (it - '0') % 2 == 0 }
	return listOf(evenCount, digits.length - evenCount)
}

