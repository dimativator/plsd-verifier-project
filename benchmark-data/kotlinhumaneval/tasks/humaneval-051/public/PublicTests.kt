fun main() {
    var arg00: String = "eabcdzzzz"
    var arg01: String = "dddzzzzzzzddeddabc"
    var x0: Boolean = sameChars(arg00, arg01)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
