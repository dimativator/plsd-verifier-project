fun findMax(words : List<String>) : String {
    var maxUniqueCharsWord = ""
    var maxUniqueCharsCount = 0

    for (word in words) {
        val uniqueCharsCount = word.toSet().size
        if (uniqueCharsCount > maxUniqueCharsCount ||
            (uniqueCharsCount == maxUniqueCharsCount && word < maxUniqueCharsWord)) {
            maxUniqueCharsCount = uniqueCharsCount
            maxUniqueCharsWord = word
        }
    }

    return maxUniqueCharsWord
}

