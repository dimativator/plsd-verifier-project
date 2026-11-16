fun main() {
    var arg00: List<Int> = mutableListOf(4, 2, 3)
    var x0: List<Int> = pluck(arg00)
    var v0: List<Int> = mutableListOf(2, 1)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
