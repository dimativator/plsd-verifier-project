fun rollingMax(numbers: List<Int>): List<Int> {
    return numbers.runningFold(0) { mx, value -> Math.max(mx, value) }.drop(1)
}

