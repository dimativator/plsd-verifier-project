fun main() {
    var arg00: List<Int> = mutableListOf(1, 4, 3, 34, 653, 2, 5)
    var arg01: List<Int> = mutableListOf(5, 7, 1, 5, 9, 653, 121)
    var x0: List<Int> = common(arg00, arg01)
    var v0: List<Int> = mutableListOf(1, 5, 653)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(5, 3, 2, 8)
    var arg11: List<Int> = mutableListOf(3, 2)
    var x1: List<Int> = common(arg10, arg11)
    var v1: List<Int> = mutableListOf(2, 3)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(4, 3, 2, 8)
    var arg21: List<Int> = mutableListOf(3, 2, 4)
    var x2: List<Int> = common(arg20, arg21)
    var v2: List<Int> = mutableListOf(2, 3, 4)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(4, 3, 2, 8)
    var arg31: List<Int> = mutableListOf()
    var x3: List<Int> = common(arg30, arg31)
    var v3: List<Int> = mutableListOf()
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

