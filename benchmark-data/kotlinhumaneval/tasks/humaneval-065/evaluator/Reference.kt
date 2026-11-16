fun pluck(arr: List<Int>): List<Int> {
    // Filter the list to get even numbers along with their indices
    val evenNumbersWithIndices = arr.withIndex()
        .filter { it.value % 2 == 0 }
        .map { Pair(it.value, it.index) }

    // Find the smallest even number (if Int)
    val smallestEven = evenNumbersWithIndices.minByOrNull { it.first }

    // Return the result according to the presence of an even number
    return if (smallestEven != null) listOf(smallestEven.first, smallestEven.second) else emptyList()
}

