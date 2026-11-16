fun main() {
    var arg00: List<Any> = mutableListOf()
    var arg01: Int = 7
    var x0: List<Any> = intersperse(arg00, arg01)
    var v0: List<Any> = mutableListOf()
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Any> = mutableListOf(5, 6, 3, 2)
    var arg11: Int = 8
    var x1: List<Any> = intersperse(arg10, arg11)
    var v1: List<Any> = mutableListOf(5, 8, 6, 8, 3, 8, 2)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Any> = mutableListOf(2, 2, 2)
    var arg21: Int = 2
    var x2: List<Any> = intersperse(arg20, arg21)
    var v2: List<Any> = mutableListOf(2, 2, 2, 2, 2)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

