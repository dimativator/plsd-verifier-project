fun main() {
    var arg00: Double = 3.5
    var x0: Double = truncateNumber(arg00)
    var v0: Double = 0.5
    if (Math.abs(x0 - v0) > 1e-9) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Double = 1.33
    var x1: Double = truncateNumber(arg10)
    var v1: Double = 0.33
    if (Math.abs(x1 - v1) > 1e-9) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Double = 123.456
    var x2: Double = truncateNumber(arg20)
    var v2: Double = 0.456
    if (Math.abs(x2 - v2) > 1e-9) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }
}
