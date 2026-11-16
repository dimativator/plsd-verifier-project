fun totalMatch(lst1: List<String>, lst2: List<String>): List<String> {
    val totalCharsLst1 = lst1.sumOf { it.length }
    val totalCharsLst2 = lst2.sumOf { it.length }

    return if (totalCharsLst1 <= totalCharsLst2) lst1 else lst2
}

