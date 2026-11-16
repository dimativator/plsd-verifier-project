fun reverseDelete(s : String, c : String) : Pair<String, Boolean> {
	val cleanedString = s.filter { it !in c }
    return Pair(cleanedString, cleanedString == cleanedString.reversed())
}

