fun greatestCommonDivisor(a: Int, b: Int): Int {
    if (b == 0) {
        return a
    }
    return greatestCommonDivisor(b, a % b)
}

