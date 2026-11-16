fun sortArrayByBinary(array: List<Int>): List<Int> {
    if (array.size == 0) {
        return emptyList()
    }
    if ((array.first() + array.last()) % 2 == 0) {
        return array.sortedDescending()
    }
    return array.sorted()
}

