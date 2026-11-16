fun allPrefixes(string: String): List<Any> {
    return string.indices.map { index ->
        string.substring(0, index + 1)
    }
}

