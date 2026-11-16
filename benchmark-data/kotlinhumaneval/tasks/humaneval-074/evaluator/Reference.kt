fun iscube(a: Int): Boolean {
    for (i in 0..Math.abs(a)) {
        val cube = i * i * i
        if (cube == Math.abs(a)) {
            return true
        }
        if (cube > Math.abs(a)) {
            return false
        }
    }
    return false
}

