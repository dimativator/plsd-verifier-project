fun histogram(text : String) : Map<String, Int> {
    if (text.isEmpty()) return emptyMap()

    val counts = text.split(" ")
        .filter { it.isNotEmpty() } // Remove any empty strings resulting from extra spaces
        .groupingBy { it }
        .eachCount()

    val maxCount = counts.maxByOrNull { it.value }?.value ?: return emptyMap()
    return counts.filter { it.value == maxCount }
}

