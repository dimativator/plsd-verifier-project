fun nextSmallest(lst: List<Int>): Int? {
    val sortedValues = lst.toSortedSet()
    if (sortedValues.size <= 1) {
        return null
    }
    return sortedValues.take(2).last()
}

