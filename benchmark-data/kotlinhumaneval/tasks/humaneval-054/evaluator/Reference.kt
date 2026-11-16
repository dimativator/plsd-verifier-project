fun monotonic(l: List<Int>): Boolean {
    val lSorted = l.sorted()
    return l == lSorted || l == lSorted.reversed()
}

