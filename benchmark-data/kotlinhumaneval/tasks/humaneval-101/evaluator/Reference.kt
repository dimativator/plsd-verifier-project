fun uniqueDigits(x: List<Int>): List<Int> {
    return x.filter { num ->
        num.toString().all { it.digitToInt() % 2 != 0 }
    }.sorted()
}

