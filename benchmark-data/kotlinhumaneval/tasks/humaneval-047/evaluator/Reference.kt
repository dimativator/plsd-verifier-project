fun modp(n: Int, p: Int): Int {
    var answer = 1
    repeat(n) {
        answer = (answer * 2) % p
    }
    return answer
}

