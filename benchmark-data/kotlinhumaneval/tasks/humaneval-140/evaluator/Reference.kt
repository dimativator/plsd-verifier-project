fun wordsInSentence(sentence : String) : String {
    fun isPrime(num: Int): Boolean {
        if (num <= 1) {
            return false
        }
        for (i in 2..num) {
            if (i * i > num) {
                break
            }
            if (num % i == 0) {
                return false
            }
        }
        return true
    }
    val words = sentence.split(" ")
    val primeLengthWords = words.filter { isPrime(it.length) }
    return primeLengthWords.joinToString(" ")
}

