fun compare(game : List<Int>, guess : List<Int>) : List<Int> {
    return game.zip(guess) { score, guessed ->
        kotlin.math.abs(score - guessed)
    }
}

