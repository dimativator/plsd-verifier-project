fun rescaleToUnit(numbers: List<Double>): List<Double> {
    val min = numbers.min()
    val max = numbers.max()
    return numbers.map { value -> (value - min) / (max - min) }
}

