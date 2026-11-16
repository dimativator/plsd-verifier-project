fun byLength(arr: List<Int>): List<String> {
    val numberNames = mapOf(
        1 to "One", 2 to "Two", 3 to "Three", 4 to "Four",
        5 to "Five", 6 to "Six", 7 to "Seven", 8 to "Eight", 9 to "Nine"
    )

    // Filter, sort, reverse, and then map integers to their corresponding names
    return arr.filter { it in 1..9 }
        .sorted()
        .reversed()
        .mapNotNull { numberNames[it] }
}

