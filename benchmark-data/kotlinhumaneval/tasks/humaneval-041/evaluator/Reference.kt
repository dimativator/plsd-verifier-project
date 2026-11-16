fun pairsSumToZero(l: List<Int>): Boolean {
    if (l.count { it == 0 } >= 2) {
        return true
    }
    val valueSet = l.toSet()
    valueSet.forEach { value ->
        if (value != 0 && valueSet.contains(-value)) {
            return true
        }
    }
    return false
}

