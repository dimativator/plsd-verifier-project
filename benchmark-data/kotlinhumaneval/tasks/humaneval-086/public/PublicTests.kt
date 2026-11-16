fun main() {
    var arg00: String = "hi"
    var x0: String = encrypt(arg00)
    var v0: String = "lm"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
