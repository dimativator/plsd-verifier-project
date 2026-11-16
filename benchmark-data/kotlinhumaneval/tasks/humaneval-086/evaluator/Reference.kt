fun encrypt(s: String): String {
    val shift = 4
    return s.map { char ->
        val shifted = ((char - 'a' + shift) % 26) + 'a'.code
        shifted.toChar()
    }.joinToString("")
}

