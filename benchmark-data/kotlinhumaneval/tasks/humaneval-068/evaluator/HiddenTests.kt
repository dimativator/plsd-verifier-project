fun main() {
    var arg10: Int = 1
    var arg11: Int = 2
    var arg12: Int = 10
    var x1: Any = triangleArea(arg10, arg11, arg12)
    var v1: Any = -1
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 4
    var arg21: Int = 8
    var arg22: Int = 5
    var x2: Any = triangleArea(arg20, arg21, arg22)
    var v2: Any = 8.18
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 2
    var arg31: Int = 2
    var arg32: Int = 2
    var x3: Any = triangleArea(arg30, arg31, arg32)
    var v3: Any = 1.73
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 1
    var arg41: Int = 2
    var arg42: Int = 3
    var x4: Any = triangleArea(arg40, arg41, arg42)
    var v4: Any = -1
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 10
    var arg51: Int = 5
    var arg52: Int = 7
    var x5: Any = triangleArea(arg50, arg51, arg52)
    var v5: Any = 16.25
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 2
    var arg61: Int = 6
    var arg62: Int = 3
    var x6: Any = triangleArea(arg60, arg61, arg62)
    var v6: Any = -1
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 1
    var arg71: Int = 1
    var arg72: Int = 1
    var x7: Any = triangleArea(arg70, arg71, arg72)
    var v7: Any = 0.43
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: Int = 2
    var arg81: Int = 2
    var arg82: Int = 10
    var x8: Any = triangleArea(arg80, arg81, arg82)
    var v8: Any = -1
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }


}

