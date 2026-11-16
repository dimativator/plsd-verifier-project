fun main() {
    var arg00: List<Int> = mutableListOf(3, 2, 3)
    var arg01: Int = 9
    var x0: Boolean = willItFly(arg00, arg01)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(1, 2)
    var arg11: Int = 5
    var x1: Boolean = willItFly(arg10, arg11)
    var v1: Boolean = false
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(3)
    var arg21: Int = 5
    var x2: Boolean = willItFly(arg20, arg21)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(3, 2, 3)
    var arg31: Int = 1
    var x3: Boolean = willItFly(arg30, arg31)
    var v3: Boolean = false
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(1, 2, 3)
    var arg41: Int = 6
    var x4: Boolean = willItFly(arg40, arg41)
    var v4: Boolean = false
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(5)
    var arg51: Int = 5
    var x5: Boolean = willItFly(arg50, arg51)
    var v5: Boolean = true
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

