fun sumProduct(numbers: List<Int>): List<Int> {
    val sum = numbers.sum()
    val prod = numbers.fold(1) { prod, value -> prod * value }
    return listOf(sum, prod)
}

