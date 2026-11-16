fun main() {
    var arg00: Any = 2
    var arg01: Any = 3
    var arg02: Any = 1
    var x0: Boolean = anyInt(arg00, arg01, arg02)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
