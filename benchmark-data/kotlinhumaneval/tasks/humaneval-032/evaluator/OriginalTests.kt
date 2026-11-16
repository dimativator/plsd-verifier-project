fun main() {
    var arg00: List<Int> = mutableListOf(1, 2, 3)
    var x0: List<Int> = sortThird(arg00)
    var v0: List<Int> = mutableListOf(1, 2, 3)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10)
    var x1: List<Int> = sortThird(arg10)
    var v1: List<Int> = mutableListOf(1, 3, -5, 2, -3, 3, 5, 0, 123, 9, -10)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(5, 8, -12, 4, 23, 2, 3, 11, 12, -10)
    var x2: List<Int> = sortThird(arg20)
    var v2: List<Int> = mutableListOf(-10, 8, -12, 3, 23, 2, 4, 11, 12, 5)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(5, 6, 3, 4, 8, 9, 2)
    var x3: List<Int> = sortThird(arg30)
    var v3: List<Int> = mutableListOf(2, 6, 3, 4, 8, 9, 5)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(5, 8, 3, 4, 6, 9, 2)
    var x4: List<Int> = sortThird(arg40)
    var v4: List<Int> = mutableListOf(2, 8, 3, 4, 6, 9, 5)
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(5, 6, 9, 4, 8, 3, 2)
    var x5: List<Int> = sortThird(arg50)
    var v5: List<Int> = mutableListOf(2, 6, 9, 4, 8, 3, 5)
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(5, 6, 3, 4, 8, 9, 2, 1)
    var x6: List<Int> = sortThird(arg60)
    var v6: List<Int> = mutableListOf(2, 6, 3, 4, 8, 9, 5, 1)
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

