fun hexKey(num: String): Int {
    val primeHexDigits = setOf('2', '3', '5', '7', 'B', 'D')
    return num.count { it in primeHexDigits }
}

