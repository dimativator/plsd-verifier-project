fun getClosestVowel(word: String): String {
    val vowels = setOf('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
    val position = word.indices.reversed().firstOrNull { ind ->
        0 < ind && ind < word.length - 1 && word[ind] in vowels && word[ind - 1] !in vowels && word[ind + 1] !in vowels
    }
    return if (position != null) {
        word[position].toString()
    } else {
        ""
    }
}

