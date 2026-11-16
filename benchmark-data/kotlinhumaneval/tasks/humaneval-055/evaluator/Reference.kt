fun common(l1: List<Int>, l2: List<Int>): List<Int> {
    return l1.toSet().intersect(l2.toSet()).toList().sorted()
}

