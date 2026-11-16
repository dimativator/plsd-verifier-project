fun specialfilter(nums : List<Int>) : Int {
    val oddDigits = setOf('1', '3', '5', '7', '9')
	return nums.count { it > 10 && it.toString().first() in oddDigits && it.toString().last() in oddDigits }
}

