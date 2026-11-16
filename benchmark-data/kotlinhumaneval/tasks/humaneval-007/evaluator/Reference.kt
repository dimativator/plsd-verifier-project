fun filterBySubstring(strings: List<String>, substring: String): List<String> {
    return strings.filter { it.contains(substring) }
}

