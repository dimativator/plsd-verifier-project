fun main() {
    var arg10: Int = 1101
    var arg11: Int = 101
    var x1: Int = modp(arg10, arg11)
    var v1: Int = 2
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 0
    var arg21: Int = 101
    var x2: Int = modp(arg20, arg21)
    var v2: Int = 1
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 3
    var arg31: Int = 11
    var x3: Int = modp(arg30, arg31)
    var v3: Int = 8
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 100
    var arg41: Int = 101
    var x4: Int = modp(arg40, arg41)
    var v4: Int = 1
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 30
    var arg51: Int = 5
    var x5: Int = modp(arg50, arg51)
    var v5: Int = 4
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 31
    var arg61: Int = 5
    var x6: Int = modp(arg60, arg61)
    var v6: Int = 3
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

