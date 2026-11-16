fun main() {
    var arg00 : List<Double> = mutableListOf(1.0, 2.0, 3.0)
    var x0 : Int = sumSquares(arg00);
    var v0 : Int = 14;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
