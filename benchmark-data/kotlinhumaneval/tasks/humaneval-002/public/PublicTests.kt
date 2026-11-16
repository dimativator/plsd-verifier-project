fun main() {
    var arg00: Double = 3.5
    var x0: Double = truncateNumber(arg00)
    var v0: Double = 0.5
    if (Math.abs(x0 - v0) > 1e-9) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
