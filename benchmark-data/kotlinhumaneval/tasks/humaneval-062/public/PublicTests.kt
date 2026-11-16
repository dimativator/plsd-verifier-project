fun main() {
    var arg00: Int = 100
    var arg01: Int = 2
    var x0: String = circularShift(arg00, arg01)
    var v0: String = "001"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
