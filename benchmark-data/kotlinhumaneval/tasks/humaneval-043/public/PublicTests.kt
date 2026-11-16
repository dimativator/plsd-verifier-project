fun main() {
    var arg00: Int = 5
    var arg01: Int = 3
    var x0: Double = triangleArea(arg00, arg01)
    var v0: Double = 7.5
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
