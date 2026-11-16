fun findClosestElements(numbers: List<Double>): List<Double> {
    return numbers.sorted().zipWithNext().sortedBy { (a, b) -> (b - a) }.first().toList()
}

