fun selectWords(s : String, n : Int) : List<Any> {
    val vowels = setOf('a', 'e', 'i', 'o', 'u')
    return s.split(" ").filter { word -> word.lowercase().count { c -> c !in vowels } == n }
}

