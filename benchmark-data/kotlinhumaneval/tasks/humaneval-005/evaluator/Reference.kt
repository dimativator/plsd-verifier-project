fun intersperse(numbers: List<Any>, delimeter: Int): List<Any> {
    return numbers.flatMapIndexed { index, value ->
        if (index == 0) {
            listOf(value)
        } else {
            listOf(delimeter, value)
        }
    }
}

