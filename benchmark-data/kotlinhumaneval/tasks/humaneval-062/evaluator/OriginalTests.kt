fun main() {
    var arg00: Int = 100
    var arg01: Int = 2
    var x0: String = circularShift(arg00, arg01)
    var v0: String = "001"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 12
    var arg11: Int = 2
    var x1: String = circularShift(arg10, arg11)
    var v1: String = "12"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 97
    var arg21: Int = 8
    var x2: String = circularShift(arg20, arg21)
    var v2: String = "79"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 12
    var arg31: Int = 1
    var x3: String = circularShift(arg30, arg31)
    var v3: String = "21"
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 11
    var arg41: Int = 101
    var x4: String = circularShift(arg40, arg41)
    var v4: String = "11"
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

