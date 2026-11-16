fun main() {
    var arg10: Int = 19
    var arg11: Int = 28
    var x1: Int = multiply(arg10, arg11)
    var v1: Int = 72
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 2020
    var arg21: Int = 1851
    var x2: Int = multiply(arg20, arg21)
    var v2: Int = 0
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 14
    var arg31: Int = -15
    var x3: Int = multiply(arg30, arg31)
    var v3: Int = 20
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 76
    var arg41: Int = 67
    var x4: Int = multiply(arg40, arg41)
    var v4: Int = 42
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 17
    var arg51: Int = 27
    var x5: Int = multiply(arg50, arg51)
    var v5: Int = 49
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 0
    var arg61: Int = 1
    var x6: Int = multiply(arg60, arg61)
    var v6: Int = 0
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 0
    var arg71: Int = 0
    var x7: Int = multiply(arg70, arg71)
    var v7: Int = 0
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

