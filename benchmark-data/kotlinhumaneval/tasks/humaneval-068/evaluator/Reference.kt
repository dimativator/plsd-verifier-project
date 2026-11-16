fun triangleArea(a: Int, b: Int, c: Int): Any {
    if (a + b <= c || a + c <= b || b + c <= a) {
        return -1
    }

    val s = (a + b + c) / 2.0
    val area = Math.sqrt(s * (s - a) * (s - b) * (s - c))
    return String.format("%.2f", area).toDouble()
}

