fun main() {
    var arg10: List<Int> = mutableListOf(1, 2, 3)
    var x1: List<Int> = pluck(arg10)
    var v1: List<Int> = mutableListOf(2, 1)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf()
    var x2: List<Int> = pluck(arg20)
    var v2: List<Int> = mutableListOf()
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(5, 0, 3, 0, 4, 2)
    var x3: List<Int> = pluck(arg30)
    var v3: List<Int> = mutableListOf(0, 1)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(1, 2, 3, 0, 5, 3)
    var x4: List<Int> = pluck(arg40)
    var v4: List<Int> = mutableListOf(0, 3)
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(5, 4, 8, 4, 8)
    var x5: List<Int> = pluck(arg50)
    var v5: List<Int> = mutableListOf(4, 1)
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(7, 6, 7, 1)
    var x6: List<Int> = pluck(arg60)
    var v6: List<Int> = mutableListOf(6, 1)
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: List<Int> = mutableListOf(7, 9, 7, 1)
    var x7: List<Int> = pluck(arg70)
    var v7: List<Int> = mutableListOf()
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

