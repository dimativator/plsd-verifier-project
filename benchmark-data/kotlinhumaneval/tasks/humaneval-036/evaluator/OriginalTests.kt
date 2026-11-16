fun main() {
    var arg00: List<Int> = mutableListOf(1, 2, 3)
    var x0: List<Int> = sortEven(arg00)
    var v0: List<Int> = mutableListOf(1, 2, 3)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10)
    var x1: List<Int> = sortEven(arg10)
    var v1: List<Int> = mutableListOf(-10, 3, -5, 2, -3, 3, 5, 0, 9, 1, 123)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(5, 8, -12, 4, 23, 2, 3, 11, 12, -10)
    var x2: List<Int> = sortEven(arg20)
    var v2: List<Int> = mutableListOf(-12, 8, 3, 4, 5, 2, 12, 11, 23, -10)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

