fun howManyTimes(string: String, substring: String): Int {
    return string.indices.count { startIndex ->
        val endIndex = startIndex + substring.length
        if (endIndex > string.length) {
            false
        } else {
            string.substring(startIndex, endIndex) == substring
        }
    }
}

