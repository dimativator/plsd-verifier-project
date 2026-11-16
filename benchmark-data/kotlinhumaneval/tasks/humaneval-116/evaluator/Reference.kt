fun matchParens(lst : List<String>) : String {
	fun checkGood(str: String): Boolean {
        val balance = str.runningFold(0) { sum, c ->
            if (c == '(') {
                sum + 1
            } else {
                sum - 1
            }
        }
        return balance.last() == 0 && balance.min() >= 0
    }
    return if (checkGood(lst[0] + lst[1]) || checkGood(lst[1] + lst[0])) {
        "Yes"
    } else {
        "No"
    }
}

