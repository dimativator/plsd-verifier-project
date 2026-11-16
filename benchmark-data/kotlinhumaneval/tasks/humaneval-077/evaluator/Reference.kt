fun isHappy(s: String): Boolean {
    if (s.length < 3) {
        return false
    }

    for (i in 0 until s.length - 2) {
        if (s[i] == s[i + 1] || s[i] == s[i + 2] || s[i + 1] == s[i + 2]) {
            return false
        }
    }
    return true
}

