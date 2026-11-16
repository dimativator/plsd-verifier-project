fun main() {
    var arg00 : Int = 7
    var x0 : List<Int> = evenOddCount(arg00);
    var v0 : List<Int> = mutableListOf(0, 1);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
