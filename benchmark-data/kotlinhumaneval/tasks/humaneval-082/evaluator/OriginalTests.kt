fun main() {
    var arg00: List<Int> = mutableListOf(4, 88)
    var x0: Int = add(arg00)
    var v0: Int = 88
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(4, 5, 6, 7, 2, 122)
    var x1: Int = add(arg10)
    var v1: Int = 122
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(4, 0, 6, 7)
    var x2: Int = add(arg20)
    var v2: Int = 0
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(4, 4, 6, 8)
    var x3: Int = add(arg30)
    var v3: Int = 12
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

