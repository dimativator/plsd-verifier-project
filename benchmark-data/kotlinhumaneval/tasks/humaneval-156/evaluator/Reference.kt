fun eat(number : Int, need : Int, remaining : Int) : List<Int> {
	val totalEaten = if (need <= remaining) number + need else number + remaining
    val carrotsLeft = if (need <= remaining) remaining - need else 0
    return listOf(totalEaten, carrotsLeft)
}

