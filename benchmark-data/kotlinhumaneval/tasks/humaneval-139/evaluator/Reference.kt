fun sumSquares(lst : List<Int>) : Int {
    return lst.mapIndexed { index, value ->
        when {
            index % 3 == 0 -> value * value
            index % 4 == 0 -> value * value * value
            else -> value
        }
    }.sum()
}

