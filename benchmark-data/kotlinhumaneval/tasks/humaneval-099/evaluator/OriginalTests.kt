fun main() {
    var arg00: Int = 12
    var arg01: Int = 15
    var x0: Int = chooseNum(arg00, arg01)
    var v0: Int = 14
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 13
    var arg11: Int = 12
    var x1: Int = chooseNum(arg10, arg11)
    var v1: Int = -1
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 33
    var arg21: Int = 12354
    var x2: Int = chooseNum(arg20, arg21)
    var v2: Int = 12354
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 5234
    var arg31: Int = 5233
    var x3: Int = chooseNum(arg30, arg31)
    var v3: Int = -1
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 6
    var arg41: Int = 29
    var x4: Int = chooseNum(arg40, arg41)
    var v4: Int = 28
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 27
    var arg51: Int = 10
    var x5: Int = chooseNum(arg50, arg51)
    var v5: Int = -1
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 7
    var arg61: Int = 7
    var x6: Int = chooseNum(arg60, arg61)
    var v6: Int = -1
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 546
    var arg71: Int = 546
    var x7: Int = chooseNum(arg70, arg71)
    var v7: Int = 546
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

