fun main() {
    var arg00: List<Double> = mutableListOf(1.0, 2.0, 3.0)
    var x0: Double = meanAbsoluteDeviation(arg00)
    var v0: Double = 0.6666666666666666
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Double> = mutableListOf(1.0, 2.0, 3.0, 4.0)
    var x1: Double = meanAbsoluteDeviation(arg10)
    var v1: Double = 1.0
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Double> = mutableListOf(1.0, 2.0, 3.0, 4.0, 5.0)
    var x2: Double = meanAbsoluteDeviation(arg20)
    var v2: Double = 1.2
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

