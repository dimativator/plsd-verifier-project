fun main() {
    var arg00: List<Int> = mutableListOf()
    var x0: Boolean = belowZero(arg00)
    var v0: Boolean = false
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(1, 2, -3, 1, 2, -3)
    var x1: Boolean = belowZero(arg10)
    var v1: Boolean = false
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(1, 2, -4, 5, 6)
    var x2: Boolean = belowZero(arg20)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(1, -1, 2, -2, 5, -5, 4, -4)
    var x3: Boolean = belowZero(arg30)
    var v3: Boolean = false
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(1, -1, 2, -2, 5, -5, 4, -5)
    var x4: Boolean = belowZero(arg40)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(1, -2, 2, -2, 5, -5, 4, -4)
    var x5: Boolean = belowZero(arg50)
    var v5: Boolean = true
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

