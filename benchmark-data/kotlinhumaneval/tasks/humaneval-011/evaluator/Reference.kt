fun stringXor(a: String, b: String): String {
    return a.indices.map { index ->
        if (a[index] == b[index]) '0' else '1'
    }.joinToString("")
}

