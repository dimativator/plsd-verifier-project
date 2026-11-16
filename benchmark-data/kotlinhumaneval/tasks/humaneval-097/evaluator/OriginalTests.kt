fun main() {
    var arg00: Int = 3
    var x0: List<Int> = makeAPile(arg00)
    var v0: List<Int> = mutableListOf(3, 5, 7)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 4
    var x1: List<Int> = makeAPile(arg10)
    var v1: List<Int> = mutableListOf(4, 6, 8, 10)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 5
    var x2: List<Int> = makeAPile(arg20)
    var v2: List<Int> = mutableListOf(5, 7, 9, 11, 13)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 6
    var x3: List<Int> = makeAPile(arg30)
    var v3: List<Int> = mutableListOf(6, 8, 10, 12, 14, 16)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 8
    var x4: List<Int> = makeAPile(arg40)
    var v4: List<Int> = mutableListOf(8, 10, 12, 14, 16, 18, 20, 22)
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }
}

