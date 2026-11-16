fun evenOddPalindrome(n : Int) : List<Int> {
    fun checkPalindrome(num: Int): Boolean {
        return num.toString() == num.toString().reversed()
    }
	val countEven = (1..n).count { it % 2 == 0 && checkPalindrome(it) }
    val countOdd = (1..n).count { it % 2 == 1 && checkPalindrome(it) }
    return listOf(countEven, countOdd)
}

