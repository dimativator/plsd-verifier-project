fun checkIfLastCharIsALetter(txt: String): Boolean {
    fun alphabeticChar(c: Char) = 'a' <= c.lowercaseChar() && c.lowercaseChar() <= 'z'
    return txt.isNotEmpty() && alphabeticChar(txt.last()) && (txt.length == 1 || !alphabeticChar(txt[txt.length - 2]))
}

