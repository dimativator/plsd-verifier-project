fun chooseNum(x: Int, y: Int): Int {
    if (x > y) {
        return -1
    }
    if (y % 2 == 0) {
        return y
    }
    if (x < y) {
        return y - 1
    }
    return -1
}

