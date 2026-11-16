fun flipCase(string: String): String {
    return string.map { char ->
        if (char.isLowerCase()) {
            char.uppercase()
        } else {
            char.lowercase()
        }
    }.joinToString("")
}

