fun correctBracketing2(brackets: String): Boolean {
    val balance = brackets.runningFold(0) { balance, c ->
        when (c) {
            '(' -> balance + 1
            ')' -> balance - 1
            else -> throw Exception("Illegal symbol")
        }
    }
    return balance.last() == 0 && balance.min() >= 0
}

