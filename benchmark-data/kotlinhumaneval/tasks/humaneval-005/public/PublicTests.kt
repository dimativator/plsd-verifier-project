fun main() {
    var arg00: List<Any> = mutableListOf()
    var arg01: Int = 7
    var x0: List<Any> = intersperse(arg00, arg01)
    var v0: List<Any> = mutableListOf()
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
