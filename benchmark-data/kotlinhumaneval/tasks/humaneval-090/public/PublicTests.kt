fun main() {
    var arg00: String = "TEST"
    var x0: String = encode(arg00)
    var v0: String = "tgst"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
