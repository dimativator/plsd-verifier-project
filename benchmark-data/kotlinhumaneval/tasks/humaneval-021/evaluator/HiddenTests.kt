fun main() {
    var arg10: List<Double> = mutableListOf(100.0, 49.9)
    var x1: List<Double> = rescaleToUnit(arg10)
    var v1: List<Double> = mutableListOf(1.0, 0.0)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Double> = mutableListOf(1.0, 2.0, 3.0, 4.0, 5.0)
    var x2: List<Double> = rescaleToUnit(arg20)
    var v2: List<Double> = mutableListOf(0.0, 0.25, 0.5, 0.75, 1.0)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Double> = mutableListOf(2.0, 1.0, 5.0, 3.0, 4.0)
    var x3: List<Double> = rescaleToUnit(arg30)
    var v3: List<Double> = mutableListOf(0.25, 0.0, 1.0, 0.5, 0.75)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Double> = mutableListOf(12.0, 11.0, 15.0, 13.0, 14.0)
    var x4: List<Double> = rescaleToUnit(arg40)
    var v4: List<Double> = mutableListOf(0.25, 0.0, 1.0, 0.5, 0.75)
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

