fun getRow(lst: List<List<Int>>, x: Int): List<List<Int>> {
    val coordinates = mutableListOf<List<Int>>()
    lst.forEachIndexed { row, ints ->
        ints.forEachIndexed { col, value ->
            if (value == x) {
                coordinates.add(listOf(row, col))
            }
        }
    }
    return coordinates
}

