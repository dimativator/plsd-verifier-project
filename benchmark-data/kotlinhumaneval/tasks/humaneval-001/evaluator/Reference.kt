fun separateParenGroups(parenString: String): List<String> {
    var balance: Int = 0
    var currentString: String = ""
    val answer = mutableListOf<String>()
    parenString.forEachIndexed { index, char ->
        if (char == '(') {
            currentString += char
            balance++
        } else if (char == ')') {
            currentString += char
            balance--
            if (balance == 0) {
                answer.add(currentString)
                currentString = ""
            }
        }
    }
    return answer
}

