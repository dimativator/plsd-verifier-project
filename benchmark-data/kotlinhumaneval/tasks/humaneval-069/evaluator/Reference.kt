fun willItFly(q: List<Int>, w: Int): Boolean {
    val isPalindromic = q == q.reversed()
    val sum = q.sum()
    return isPalindromic && sum <= w
}

