fun strangeSortList(lst: List<Int>): List<Int> {
    if (lst.isEmpty()) return lst

    val sortedList = lst.sorted().toMutableList()
    val result = mutableListOf<Int>()
    var addingMinimum = true

    while (sortedList.isNotEmpty()) {
        if (addingMinimum) {
            result.add(sortedList.removeAt(0))
        } else {
            result.add(sortedList.removeAt(sortedList.size - 1))
        }
        addingMinimum = !addingMinimum
    }

    return result
}

