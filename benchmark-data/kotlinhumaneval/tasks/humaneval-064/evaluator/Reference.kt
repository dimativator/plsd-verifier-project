fun fruitDistribution(s: String, totalFruits: Int): Int {
    // Extract the numbers from the string
    val numbers = s.split(" ").filter { it.toIntOrNull() != null }.map { it.toInt() }
    // Assuming the string format is always "<number> apples and <number> oranges"
    val apples = numbers[0]
    val oranges = numbers[1]

    // Calculate the number of mangoes
    return totalFruits - apples - oranges
}

