fun countNums(arr: List<Int>): Int {
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
    return arr.count { countDigitSum(it) > 0 }
}

