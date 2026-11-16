fun main() {
    var arg00: List<Int> = mutableListOf(1, 2, 3, 4, 5)
    var x0: Int? = nextSmallest(arg00)
    var v0: Int? = 2
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
