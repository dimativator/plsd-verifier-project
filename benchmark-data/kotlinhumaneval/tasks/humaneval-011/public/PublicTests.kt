fun main() {
    var arg00: String = "111000"
    var arg01: String = "101010"
    var x0: String = stringXor(arg00, arg01)
    var v0: String = "010010"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
