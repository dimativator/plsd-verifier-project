fun orderByPoints(nums : List<Int>) : List<Int> {
    fun countDigitSum(num: Int): Int {
        val sign = if (num >= 0) 1 else -1
        var x = Math.abs(num)
        var digitSum = 0
        while (x > 0) {
            if (x < 10) {
                digitSum += x * sign
                break
            } else {
                digitSum += x % 10
                x /= 10
            }
        }
        return digitSum
    }
    val withSumAndIndex = nums.mapIndexed { index, num ->
        val sumOfDigits = countDigitSum(num)
        Triple(num, sumOfDigits, index)
    }
    val sorted = withSumAndIndex.sortedWith(compareBy({ it.second }, { it.third }))
    return sorted.map { it.first }
}

