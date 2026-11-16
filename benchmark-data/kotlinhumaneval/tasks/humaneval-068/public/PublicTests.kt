fun main() {
    var arg00: Int = 3
    var arg01: Int = 4
    var arg02: Int = 5
    var x0: Any = triangleArea(arg00, arg01, arg02)
    var v0: Any = 6.0
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
