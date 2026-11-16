fun hasCloseElements(numbers: List<Double>, threshold: Double): Boolean {
    return numbers.sorted().zipWithNext { a, b -> b - a <= threshold }.any { it }
}

