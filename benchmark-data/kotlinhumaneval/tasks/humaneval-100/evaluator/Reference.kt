fun roundedAvg(n: Int, m: Int): String {
    if (n > m) {
        return "-1"
    }
    return "0b" + ((n + m) / 2).toString(2)
}

