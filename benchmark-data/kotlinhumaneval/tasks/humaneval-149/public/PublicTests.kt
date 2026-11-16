fun main() {
    var arg00 : List<Int> = mutableListOf(1, 2, 3, 4, 5, 1)
    var arg01 : List<Int> = mutableListOf(1, 2, 3, 4, 2, -2)
    var x0 : List<Int> = compare(arg00, arg01);
    var v0 : List<Int> = mutableListOf(0, 0, 0, 0, 3, 3);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
