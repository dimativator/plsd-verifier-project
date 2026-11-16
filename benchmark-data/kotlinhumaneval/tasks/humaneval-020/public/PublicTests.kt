fun main() {
    var arg00: List<Double> = mutableListOf(1.0, 2.0, 3.9, 4.0, 5.0, 2.2)
    var x0: List<Double> = findClosestElements(arg00)
    var v0: List<Double> = mutableListOf(3.9, 4.0)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
