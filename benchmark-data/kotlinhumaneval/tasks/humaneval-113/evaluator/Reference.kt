fun sortArrayByBinary(arr: List<Int>): List<Int> {
    fun countOnes(num: Int) = num.toString(2).count { c -> c == '1' }
    return arr.sortedWith(
        Comparator<Int> { num1, num2 ->
            countOnes(num1).compareTo(countOnes(num2))
        }.thenBy { it }
    )
}

