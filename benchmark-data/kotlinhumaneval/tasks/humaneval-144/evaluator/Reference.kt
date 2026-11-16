fun getMaxTriples(n : Int) : Int {
    val counts = IntArray(3) { 0 }
    for (i in 1..n) {
        val value = (i * i - i + 1) % 3
        counts[value]++
    }
    val triples = (counts[0] * (counts[0] - 1) * (counts[0] - 2)) / 6 +
            (counts[1] * (counts[1] - 1) * (counts[1] - 2)) / 6 +
            (counts[2] * (counts[2] - 1) * (counts[2] - 2)) / 6 +
            counts[0] * counts[1] * counts[2]

    return triples
}

