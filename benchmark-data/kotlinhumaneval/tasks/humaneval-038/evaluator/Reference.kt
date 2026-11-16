fun triplesSumToZero(l: List<Int>): Boolean {
    val sortedList = l.sorted()
    for (i in 0 until sortedList.size - 2) {
        // Avoid duplicate elements
        if (i > 0 && sortedList[i] == sortedList[i - 1]) continue

        var left = i + 1
        var right = sortedList.size - 1
        while (left < right) {
            val sum = sortedList[i] + sortedList[left] + sortedList[right]
            if (sum == 0) {
                return true
            } else if (sum < 0) {
                left++
            } else {
                right--
            }
        }
    }
    return false
}
