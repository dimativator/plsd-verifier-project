fun main() {
    var arg00: Int = 8
    var arg01: Int = 3
    var x0: String = changeBase(arg00, arg01)
    var v0: String = "22"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 9
    var arg11: Int = 3
    var x1: String = changeBase(arg10, arg11)
    var v1: String = "100"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 234
    var arg21: Int = 2
    var x2: String = changeBase(arg20, arg21)
    var v2: String = "11101010"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 16
    var arg31: Int = 2
    var x3: String = changeBase(arg30, arg31)
    var v3: String = "10000"
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 8
    var arg41: Int = 2
    var x4: String = changeBase(arg40, arg41)
    var v4: String = "1000"
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 7
    var arg51: Int = 2
    var x5: String = changeBase(arg50, arg51)
    var v5: String = "111"
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 2
    var arg61: Int = 3
    var x6: String = changeBase(arg60, arg61)
    var v6: String = "2"
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 3
    var arg71: Int = 4
    var x7: String = changeBase(arg70, arg71)
    var v7: String = "3"
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: Int = 4
    var arg81: Int = 5
    var x8: String = changeBase(arg80, arg81)
    var v8: String = "4"
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: Int = 5
    var arg91: Int = 6
    var x9: String = changeBase(arg90, arg91)
    var v9: String = "5"
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100: Int = 6
    var arg101: Int = 7
    var x10: String = changeBase(arg100, arg101)
    var v10: String = "6"
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110: Int = 7
    var arg111: Int = 8
    var x11: String = changeBase(arg110, arg111)
    var v11: String = "7"
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }


}

