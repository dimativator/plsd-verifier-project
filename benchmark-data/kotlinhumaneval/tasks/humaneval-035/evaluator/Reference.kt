fun fizzBuzz(n: Int): Int {
    return (1 until n).map { value ->
        if (value % 11 == 0 || value % 13 == 0) {
            value.toString().count { c -> c == '7' }
        } else {
            0
        }
    }.sum()
}

