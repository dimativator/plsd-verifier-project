fun main() {
    var arg00: List<Int> = mutableListOf(5, 3, 5, 2, 3, 3, 9, 0, 123)
    var x0: List<Int> = unique(arg00)
    var v0: List<Int> = mutableListOf(0, 2, 3, 5, 9, 123)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }


}

