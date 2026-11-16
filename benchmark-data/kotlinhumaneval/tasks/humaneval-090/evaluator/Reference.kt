fun encode(message: String): String {
    val vowelMap = mapOf(
        'a' to 'c', 'A' to 'C',
        'e' to 'g', 'E' to 'G',
        'i' to 'k', 'I' to 'K',
        'o' to 'q', 'O' to 'Q',
        'u' to 'w', 'U' to 'W'
    )
    return message.map { char ->
        val swappedCaseChar = if (char.isUpperCase()) {
            char.lowercaseChar()
        } else {
            char.uppercaseChar()
        }
        vowelMap.getOrDefault(swappedCaseChar, swappedCaseChar)
    }.joinToString("")
}

