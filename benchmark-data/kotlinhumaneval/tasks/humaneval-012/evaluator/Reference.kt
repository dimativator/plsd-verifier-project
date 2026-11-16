fun longest(strings: List<String>): String? {
    if (strings.isEmpty()) return null

    return strings.maxWithOrNull(compareBy { it.length })
}

