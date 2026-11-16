fun removeDuplicates(numbers: List<Int>): List<Int> {
    val occurrenceMap = numbers.groupingBy { it }.eachCount()
    return numbers.filter { occurrenceMap[it] == 1 }
}

