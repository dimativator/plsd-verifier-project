fun main() {
    var arg00: Int = 12
    var arg01: Int = 15
    var x0: Int = chooseNum(arg00, arg01)
    var v0: Int = 14
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
