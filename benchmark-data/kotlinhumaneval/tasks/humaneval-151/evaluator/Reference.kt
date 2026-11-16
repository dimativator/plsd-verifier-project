fun cycpatternCheck(a : String, b : String) : Boolean {
    val rotations = mutableListOf<String>()
    for (i in b.indices) {
        val rotation = b.substring(i) + b.substring(0, i)
        rotations.add(rotation)
    }
    return rotations.any { rotation -> a.contains(rotation) }
}

