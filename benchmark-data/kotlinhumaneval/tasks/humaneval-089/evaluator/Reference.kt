fun anyInt(x: Any, y: Any, z: Any): Boolean {
    if (x is Int && y is Int && z is Int) {
        return x == y + z || y == x + z || z == x + y
    }
    return false
}

