fun changeBase(x: Int, base: Int): String {
    // Handle the case when the input number is 0
    if (x == 0) return "0"

    var num = x
    val result = StringBuilder()

    while (num > 0) {
        // Prepend the remainder (digit in the new base) to the result
        result.insert(0, num % base)
        // Divide the number by the base for the next iteration
        num /= base
    }

    return result.toString()
}

