fun belowZero(operations: List<Int>): Boolean {
    return operations.runningFold(0) { sum, value ->
        sum + value
    }.any { it < 0 }
}

