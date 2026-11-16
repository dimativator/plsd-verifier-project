fun circularShift(x: Int, shift: Int): String {
    val digits = x.toString() // Convert the integer to its string representation
    val length = digits.length // Get the number of digits
    val effectiveShift = if (shift > length) length else shift % length // Calculate the effective shift

    return if (effectiveShift == length) {
        digits.reversed()
    } else {
        digits.substring(length - effectiveShift) + digits.substring(0, length - effectiveShift)
    }
}

