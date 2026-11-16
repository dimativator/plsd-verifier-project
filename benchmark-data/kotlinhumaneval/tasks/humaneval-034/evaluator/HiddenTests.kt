fun main() {
    var arg10: List<Int> = mutableListOf(5, 3, -5, 2, -3, 3, 9, 0, 124, 1, -10)
    var x1: Int = maxElement(arg10)
    var v1: Int = 124
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }


}

