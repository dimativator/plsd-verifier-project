fun add(lst: List<Int>): Int {
    var answer = 0
    lst.forEachIndexed { index, value ->
        if (index % 2 == 1 && value % 2 == 0) {
            answer += value
        }
    }
    return answer
}

