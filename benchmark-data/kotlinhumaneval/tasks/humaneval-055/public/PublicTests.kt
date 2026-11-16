fun main() {
    var arg00: List<Int> = mutableListOf(1, 4, 3, 34, 653, 2, 5)
    var arg01: List<Int> = mutableListOf(5, 7, 1, 5, 9, 653, 121)
    var x0: List<Int> = common(arg00, arg01)
    var v0: List<Int> = mutableListOf(1, 5, 653)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
