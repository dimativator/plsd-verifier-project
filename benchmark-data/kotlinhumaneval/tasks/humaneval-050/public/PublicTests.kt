fun main() {
    var arg00: Int = 0
    var arg01: Int = 1
    var x0: Int = add(arg00, arg01)
    var v0: Int = 1
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
