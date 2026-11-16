fun main() {
    var arg00: List<Double> = mutableListOf(2.0, 49.9)
    var x0: List<Double> = rescaleToUnit(arg00)
    var v0: List<Double> = mutableListOf(0.0, 1.0)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
