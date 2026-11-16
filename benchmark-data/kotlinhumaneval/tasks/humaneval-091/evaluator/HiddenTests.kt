fun main() {
    var arg10: List<Int> = mutableListOf(1, 0, 1, 8, 2, 4597, 2, 1, 3, 40, 1, 2, 1, 2, 4, 2, 5, 1)
    var x1: Int = skjkasdkd(arg10)
    var v1: Int = 25
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(1, 3, 1, 32, 5107, 34, 83278, 109, 163, 23, 2323, 32, 30, 1, 9, 3)
    var x2: Int = skjkasdkd(arg20)
    var v2: Int = 13
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(0, 724, 32, 71, 99, 32, 6, 0, 5, 91, 83, 0, 5, 6)
    var x3: Int = skjkasdkd(arg30)
    var v3: Int = 11
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(0, 81, 12, 3, 1, 21)
    var x4: Int = skjkasdkd(arg40)
    var v4: Int = 3
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(0, 8, 1, 2, 1, 7)
    var x5: Int = skjkasdkd(arg50)
    var v5: Int = 7
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(8191)
    var x6: Int = skjkasdkd(arg60)
    var v6: Int = 19
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: List<Int> = mutableListOf(8191, 123456, 127, 7)
    var x7: Int = skjkasdkd(arg70)
    var v7: Int = 19
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: List<Int> = mutableListOf(127, 97, 8192)
    var x8: Int = skjkasdkd(arg80)
    var v8: Int = 10
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }


}

