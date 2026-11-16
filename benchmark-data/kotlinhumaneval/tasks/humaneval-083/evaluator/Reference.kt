fun antiShuffle(s: String): String {
    val words = s.split(" ")
    val sortedWords = words.map { word ->
        if (word.trim().isNotEmpty()) word.toCharArray().sorted().joinToString("") else word
    }
    return sortedWords.joinToString(" ")
}

