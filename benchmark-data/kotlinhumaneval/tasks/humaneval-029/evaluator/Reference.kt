fun filterByPrefix(strings: List<String>, prefix: String): List<String> {
    return strings.filter { it.startsWith(prefix) }
}

