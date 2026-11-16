fun main() {
    var arg00: Any = 2
    var arg01: Any = 3
    var arg02: Any = 1
    var x0: Boolean = anyInt(arg00, arg01, arg02)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Any = 2.5
    var arg11: Any = 2
    var arg12: Any = 3
    var x1: Boolean = anyInt(arg10, arg11, arg12)
    var v1: Boolean = false
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Any = 1.5
    var arg21: Any = 5
    var arg22: Any = 3.5
    var x2: Boolean = anyInt(arg20, arg21, arg22)
    var v2: Boolean = false
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Any = 2
    var arg31: Any = 6
    var arg32: Any = 2
    var x3: Boolean = anyInt(arg30, arg31, arg32)
    var v3: Boolean = false
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Any = 4
    var arg41: Any = 2
    var arg42: Any = 2
    var x4: Boolean = anyInt(arg40, arg41, arg42)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Any = 2.2
    var arg51: Any = 2.2
    var arg52: Any = 2.2
    var x5: Boolean = anyInt(arg50, arg51, arg52)
    var v5: Boolean = false
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Any = -4
    var arg61: Any = 6
    var arg62: Any = 2
    var x6: Boolean = anyInt(arg60, arg61, arg62)
    var v6: Boolean = true
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Any = 2
    var arg71: Any = 1
    var arg72: Any = 1
    var x7: Boolean = anyInt(arg70, arg71, arg72)
    var v7: Boolean = true
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: Any = 3
    var arg81: Any = 4
    var arg82: Any = 7
    var x8: Boolean = anyInt(arg80, arg81, arg82)
    var v8: Boolean = true
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: Any = 3.0
    var arg91: Any = 4
    var arg92: Any = 7
    var x9: Boolean = anyInt(arg90, arg91, arg92)
    var v9: Boolean = false
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }


}

