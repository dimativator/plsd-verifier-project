fun oddCount(lst : List<String>) : List<String> {
    return lst.map { str ->
        val oddCount = str.count { it in listOf('1', '3', '5', '7', '9') }
        "the number of odd elements ${oddCount}n the str${oddCount}ng ${oddCount} of the ${oddCount}nput."
    }
}

