fun main() {
    var arg00: List<Int> = mutableListOf(3, 2, 3)
    var arg01: Int = 9
    var x0: Boolean = willItFly(arg00, arg01)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
