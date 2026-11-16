fun main() {
    var arg00 : List<Int> = mutableListOf(1, 2, 3)
    var x0 : Int = sumSquares(arg00);
    var v0 : Int = 6;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
