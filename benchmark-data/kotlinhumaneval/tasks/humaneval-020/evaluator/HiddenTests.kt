fun main() {
    var arg10: List<Double> = mutableListOf(1.0, 2.0, 5.9, 4.0, 5.0)
    var x1: List<Double> = findClosestElements(arg10)
    var v1: List<Double> = mutableListOf(5.0, 5.9)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Double> = mutableListOf(1.0, 2.0, 3.0, 4.0, 5.0, 2.2)
    var x2: List<Double> = findClosestElements(arg20)
    var v2: List<Double> = mutableListOf(2.0, 2.2)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Double> = mutableListOf(1.0, 2.0, 3.0, 4.0, 5.0, 2.0)
    var x3: List<Double> = findClosestElements(arg30)
    var v3: List<Double> = mutableListOf(2.0, 2.0)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Double> = mutableListOf(1.1, 2.2, 3.1, 4.1, 5.1)
    var x4: List<Double> = findClosestElements(arg40)
    var v4: List<Double> = mutableListOf(2.2, 3.1)
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

