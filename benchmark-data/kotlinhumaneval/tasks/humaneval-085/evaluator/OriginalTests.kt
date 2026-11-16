fun main() {
    var arg00: List<Int> = mutableListOf()
    var x0: List<Int> = sortArrayByBinary(arg00)
    var v0: List<Int> = mutableListOf()
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(5)
    var x1: List<Int> = sortArrayByBinary(arg10)
    var v1: List<Int> = mutableListOf(5)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(2, 4, 3, 0, 1, 5)
    var x2: List<Int> = sortArrayByBinary(arg20)
    var v2: List<Int> = mutableListOf(0, 1, 2, 3, 4, 5)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(2, 4, 3, 0, 1, 5, 6)
    var x3: List<Int> = sortArrayByBinary(arg30)
    var v3: List<Int> = mutableListOf(6, 5, 4, 3, 2, 1, 0)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(2, 1)
    var x4: List<Int> = sortArrayByBinary(arg40)
    var v4: List<Int> = mutableListOf(1, 2)
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(15, 42, 87, 32, 11, 0)
    var x5: List<Int> = sortArrayByBinary(arg50)
    var v5: List<Int> = mutableListOf(0, 11, 15, 32, 42, 87)
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(21, 14, 23, 11)
    var x6: List<Int> = sortArrayByBinary(arg60)
    var v6: List<Int> = mutableListOf(23, 21, 14, 11)
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

