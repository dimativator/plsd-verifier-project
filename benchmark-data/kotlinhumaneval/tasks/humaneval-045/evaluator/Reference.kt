fun median(l: List<Int>): Double {
    val sortedList = l.sorted()
    val middle = sortedList.size / 2

    return if (sortedList.size % 2 == 0) {
        (sortedList[middle - 1] + sortedList[middle]) / 2.0
    } else {
        sortedList[middle].toDouble()
    }
}

