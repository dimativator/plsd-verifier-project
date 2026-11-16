fun smallestChange(arr: List<Int>): Int {
    return arr.zip(arr.reversed()).count { (a, b) -> a != b } / 2
}

