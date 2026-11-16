fun simplify(x : String, n : String) : Boolean {
    val (numeratorX, denominatorX) = x.split("/").map { it.toInt() }
    val (numeratorN, denominatorN) = n.split("/").map { it.toInt() }

    val productNumerator = numeratorX * numeratorN
    val productDenominator = denominatorX * denominatorN

    return productNumerator % productDenominator == 0
}

