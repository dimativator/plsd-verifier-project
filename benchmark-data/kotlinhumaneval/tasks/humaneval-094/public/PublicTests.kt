fun main() {
    var arg00: Int = 148
    var arg01: Int = 412
    var x0: Int = multiply(arg00, arg01)
    var v0: Int = 16
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
