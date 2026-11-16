fun meanAbsoluteDeviation(numbers: List<Double>): Double {
    val mean = numbers.average()
    return numbers.map { Math.abs(it - mean) }.average()
}

