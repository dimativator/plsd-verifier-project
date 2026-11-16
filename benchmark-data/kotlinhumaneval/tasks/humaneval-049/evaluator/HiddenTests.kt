fun main() {
    var arg10: List<Int> = mutableListOf(1, 20, 4, 10)
    var arg11: Int = 5
    var x1: Boolean = belowThreshold(arg10, arg11)
    var v1: Boolean = false
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(1, 20, 4, 10)
    var arg21: Int = 21
    var x2: Boolean = belowThreshold(arg20, arg21)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(1, 20, 4, 10)
    var arg31: Int = 22
    var x3: Boolean = belowThreshold(arg30, arg31)
    var v3: Boolean = true
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(1, 8, 4, 10)
    var arg41: Int = 11
    var x4: Boolean = belowThreshold(arg40, arg41)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(1, 8, 4, 10)
    var arg51: Int = 10
    var x5: Boolean = belowThreshold(arg50, arg51)
    var v5: Boolean = false
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

