fun makePalindrome(string: String): String {
    for (startPosition in string.indices) {
        if (string.substring(startPosition) == string.substring(startPosition).reversed()) {
            return string + string.substring(0, startPosition).reversed()
        }
    }
    return string
}

