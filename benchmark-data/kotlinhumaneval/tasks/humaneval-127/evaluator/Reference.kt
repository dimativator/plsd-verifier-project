fun tri(n : Int) : List<Int> {
    if (n == 0) {
        return listOf(1)
    }
	val tris = mutableListOf(1, 3)
    while(tris.size <= n) {
        val ind = tris.size
        if (ind % 2 == 0) {
            tris.add(1 + ind / 2)
        } else {
            tris.add(tris[tris.size - 2] + 2 + ind)
        }
    }
    return tris
}

