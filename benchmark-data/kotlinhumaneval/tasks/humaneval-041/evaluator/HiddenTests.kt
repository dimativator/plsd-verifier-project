fun main() {
    var arg10: List<Int> = mutableListOf(1, 3, -2, 1)
    var x1: Boolean = pairsSumToZero(arg10)
    var v1: Boolean = false
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(1, 2, 3, 7)
    var x2: Boolean = pairsSumToZero(arg20)
    var v2: Boolean = false
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(2, 4, -5, 3, 5, 7)
    var x3: Boolean = pairsSumToZero(arg30)
    var v3: Boolean = true
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(1)
    var x4: Boolean = pairsSumToZero(arg40)
    var v4: Boolean = false
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(-3, 9, -1, 3, 2, 30)
    var x5: Boolean = pairsSumToZero(arg50)
    var v5: Boolean = true
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(-3, 9, -1, 3, 2, 31)
    var x6: Boolean = pairsSumToZero(arg60)
    var v6: Boolean = true
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: List<Int> = mutableListOf(-3, 9, -1, 4, 2, 30)
    var x7: Boolean = pairsSumToZero(arg70)
    var v7: Boolean = false
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: List<Int> = mutableListOf(-3, 9, -1, 4, 2, 31)
    var x8: Boolean = pairsSumToZero(arg80)
    var v8: Boolean = false
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }


}

