fun main() {
    var arg00: List<Int> = mutableListOf(1, 2, 3)
    var x0: Int = maxElement(arg00)
    var v0: Int = 3
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(5, 3, -5, 2, -3, 3, 9, 0, 124, 1, -10)
    var x1: Int = maxElement(arg10)
    var v1: Int = 124
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }


}

