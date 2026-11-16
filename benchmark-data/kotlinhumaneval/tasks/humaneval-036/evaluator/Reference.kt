fun sortEven(l: List<Int>): List<Int> {
    val sortedEvens = l.withIndex()
        .filter { (index, _) -> (index % 2) == 0 }
        .map { it.value }
        .sorted()
    return l.mapIndexed { index, value ->
        if (index % 2 == 0) sortedEvens[index / 2] else value
    }
}

