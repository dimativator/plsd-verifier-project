fun largestSmallestIntegers(lst : List<Int>) : List<Int?> {
    val negatives = lst.filter { it < 0 }
    val positives = lst.filter { it > 0 }

    val largestNegative = negatives.maxOrNull()
    val smallestPositive = positives.minOrNull()

    return listOf(largestNegative, smallestPositive)
}

