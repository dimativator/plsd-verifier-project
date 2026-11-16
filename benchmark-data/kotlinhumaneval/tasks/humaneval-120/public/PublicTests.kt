fun main() {
    var arg00 : Int = 14
    var x0 : List<Int> = getOddCollatz(arg00);
    var v0 : List<Int> = mutableListOf(1, 5, 7, 11, 13, 17);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
