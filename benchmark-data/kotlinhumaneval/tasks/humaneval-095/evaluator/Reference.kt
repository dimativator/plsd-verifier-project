fun countUpper(s: String): Int {
    val vowels = setOf('A', 'E', 'I', 'O', 'U')
    return s.filterIndexed { index, c -> index % 2 == 0 && c in vowels }.length
}

