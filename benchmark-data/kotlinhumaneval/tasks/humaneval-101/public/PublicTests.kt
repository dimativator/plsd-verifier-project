fun main() {
    var arg00: List<Int> = mutableListOf(15, 33, 1422, 1)
    var x0: List<Int> = uniqueDigits(arg00);
    var v0: List<Int> = mutableListOf(1, 15, 33);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
