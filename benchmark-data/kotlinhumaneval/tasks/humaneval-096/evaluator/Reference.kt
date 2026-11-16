fun closestInteger(value: String): Int {
    val number = value.toDouble()
    val fractionalPart = number % 1.0
    val isHalf = fractionalPart == 0.5 || fractionalPart == -0.5

    return if (isHalf) {
        if (number > 0) Math.ceil(number).toInt() else Math.floor(number).toInt()
    } else {
        Math.round(number).toInt()
    }
}

