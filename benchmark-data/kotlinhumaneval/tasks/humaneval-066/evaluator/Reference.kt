fun search(lst: List<Int>): Int {
    val frequencyMap = lst.groupingBy { it }.eachCount()
    return frequencyMap.filter { it.key <= it.value }.keys.maxOrNull() ?: -1
}
