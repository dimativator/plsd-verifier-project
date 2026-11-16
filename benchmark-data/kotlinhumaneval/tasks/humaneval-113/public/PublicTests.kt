fun main() {
    var arg00: List<Int> = mutableListOf(1, 5, 2, 3, 4)
    var x0: List<Int> = sortArrayByBinary(arg00);
    var v0: List<Int> = mutableListOf(1, 2, 4, 3, 5);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
