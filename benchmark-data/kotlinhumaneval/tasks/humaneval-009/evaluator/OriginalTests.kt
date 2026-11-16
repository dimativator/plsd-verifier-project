fun main() {
    var arg00: List<Int> = mutableListOf()
    var x0: List<Int> = rollingMax(arg00)
    var v0: List<Int> = mutableListOf()
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(1, 2, 3, 4)
    var x1: List<Int> = rollingMax(arg10)
    var v1: List<Int> = mutableListOf(1, 2, 3, 4)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(4, 3, 2, 1)
    var x2: List<Int> = rollingMax(arg20)
    var v2: List<Int> = mutableListOf(4, 4, 4, 4)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(3, 2, 3, 100, 3)
    var x3: List<Int> = rollingMax(arg30)
    var v3: List<Int> = mutableListOf(3, 3, 3, 100, 100)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

