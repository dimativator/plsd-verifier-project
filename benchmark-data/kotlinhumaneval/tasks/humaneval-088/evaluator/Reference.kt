fun isBored(s: String): Int {
    return s.split("[.?!]\\W*".toRegex()).count { it.startsWith("I ") }
}

