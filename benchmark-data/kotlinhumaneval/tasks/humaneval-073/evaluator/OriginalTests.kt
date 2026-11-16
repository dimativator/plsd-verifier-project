fun main() {
    var arg00: Int = 16
    var arg01: Int = 2
    var x0: Boolean = isSimplePower(arg00, arg01)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 143214
    var arg11: Int = 16
    var x1: Boolean = isSimplePower(arg10, arg11)
    var v1: Boolean = false
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 4
    var arg21: Int = 2
    var x2: Boolean = isSimplePower(arg20, arg21)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 9
    var arg31: Int = 3
    var x3: Boolean = isSimplePower(arg30, arg31)
    var v3: Boolean = true
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 16
    var arg41: Int = 4
    var x4: Boolean = isSimplePower(arg40, arg41)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 24
    var arg51: Int = 2
    var x5: Boolean = isSimplePower(arg50, arg51)
    var v5: Boolean = false
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 128
    var arg61: Int = 4
    var x6: Boolean = isSimplePower(arg60, arg61)
    var v6: Boolean = false
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 12
    var arg71: Int = 6
    var x7: Boolean = isSimplePower(arg70, arg71)
    var v7: Boolean = false
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: Int = 1
    var arg81: Int = 1
    var x8: Boolean = isSimplePower(arg80, arg81)
    var v8: Boolean = true
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: Int = 1
    var arg91: Int = 12
    var x9: Boolean = isSimplePower(arg90, arg91)
    var v9: Boolean = true
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }


}

