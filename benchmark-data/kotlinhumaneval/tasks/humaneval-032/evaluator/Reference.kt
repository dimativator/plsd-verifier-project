fun sortThird(l: List<Int>): List<Int> {
    val sortedThirds = l.withIndex()
        .filter { (index, _) -> (index % 3) == 0 }
        .map { it.value }
        .sorted()
    return l.mapIndexed { index, value ->
        if (index % 3 == 0) sortedThirds[index / 3] else value
    }
}

