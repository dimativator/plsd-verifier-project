fun main() {
    var arg00: Int = 3
    var arg01: Int = 5
    var x0: Int = modp(arg00, arg01)
    var v0: Int = 3
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
