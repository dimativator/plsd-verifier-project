fun main() {
    var arg00: List<Int> = mutableListOf(1, 2, 3, 4)
    var x0: List<Int> = strangeSortList(arg00)
    var v0: List<Int> = mutableListOf(1, 4, 2, 3)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
