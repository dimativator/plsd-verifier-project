fun digits(n : Int) : Int {
    val oddDigitsProduct = n.toString()
        .filter { it.digitToInt() % 2 != 0 }
        .map { it.toString().toInt() }
        .fold(1) { acc, i -> acc * i }

    return if (oddDigitsProduct == 1 && n.toString().all { it.digitToInt() % 2 == 0 }) 0 else oddDigitsProduct
}

