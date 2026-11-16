fun solve(s : String) : String {
    val containsLetters = s.any { it.isLetter() }
    if (!containsLetters) {
        return s.reversed()
    }
    return s.map { char ->
        when {
            char.isUpperCase() -> char.lowercase()
            char.isLowerCase() -> char.uppercase()
            else -> char.toString()
        }
    }.joinToString("")
}

