fun vowelsCount(s: String): Int {
    val vowels = setOf('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
    return s.count { it in vowels } + if (s.last().lowercase() == "y") 1 else 0
}

