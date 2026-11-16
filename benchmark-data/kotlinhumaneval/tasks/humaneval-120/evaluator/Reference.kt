fun getOddCollatz(n : Int) : List<Int> {
    var current = n
    val oddNumbers = mutableSetOf<Int>()

    while (current != 1) {
        if (current % 2 != 0) oddNumbers.add(current)
        current = if (current % 2 == 0) {
            current / 2
        } else {
            3 * current + 1
        }
    }
    oddNumbers.add(1)
    return oddNumbers.sorted()
}

