fun wordsString(s: String): List<String> {
    return s.split("[, ]+".toRegex()).filterNot { it.isEmpty() }
}

