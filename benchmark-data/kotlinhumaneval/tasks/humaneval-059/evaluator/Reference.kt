fun derivative(xs: List<Int>): List<Int> {
    return xs.mapIndexed { index, value ->
        value * index
    }.drop(1)
}

