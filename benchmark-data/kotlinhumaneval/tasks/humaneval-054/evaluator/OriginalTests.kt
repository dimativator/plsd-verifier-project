fun main() {
    var arg00: List<Int> = mutableListOf(1, 2, 4, 10)
    var x0: Boolean = monotonic(arg00)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(1, 2, 4, 20)
    var x1: Boolean = monotonic(arg10)
    var v1: Boolean = true
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(1, 20, 4, 10)
    var x2: Boolean = monotonic(arg20)
    var v2: Boolean = false
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(4, 1, 0, -10)
    var x3: Boolean = monotonic(arg30)
    var v3: Boolean = true
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(4, 1, 1, 0)
    var x4: Boolean = monotonic(arg40)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(1, 2, 3, 2, 5, 60)
    var x5: Boolean = monotonic(arg50)
    var v5: Boolean = false
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(1, 2, 3, 4, 5, 60)
    var x6: Boolean = monotonic(arg60)
    var v6: Boolean = true
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: List<Int> = mutableListOf(9, 9, 9, 9)
    var x7: Boolean = monotonic(arg70)
    var v7: Boolean = true
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

