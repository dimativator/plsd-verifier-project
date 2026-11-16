fun countDistinctCharacters(string: String): Int {
    return string.lowercase().toSet().size
}

