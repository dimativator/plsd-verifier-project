fun isNested(string : String) : Boolean {
    var depth = 0
    var foundNest = false
    for (char in string) {
        when (char) {
            '[' -> depth++
            ']' -> depth--
        }
        if (depth > 1) foundNest = true
        if (depth == 0 && foundNest) return true
    }
    return false
}

