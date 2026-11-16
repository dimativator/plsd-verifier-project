fun parseNestedParens(parenString: String): List<Int> {
    return parenString.split(" ").map {
        it.runningFold(0) { balance, char ->
            when (char) {
                '(' -> {
                    balance + 1
                }

                ')' -> {
                    balance - 1
                }

                else -> {
                    throw Exception("Invalid character")
                }
            }
        }.max()
    }
}

