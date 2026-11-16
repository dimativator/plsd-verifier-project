fun digitsum(s: String): Int {
    return s.filter { it.isUpperCase() }.map { it.code }.sum()
}

