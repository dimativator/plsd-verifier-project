fun main() {
    var arg00 : List<List<Int>> = mutableListOf(mutableListOf(1, 2, 3), mutableListOf(4, 5, 6), mutableListOf(7, 8, 9))
    var arg01 : Int = 3
    var x0 : List<Int> = minpath(arg00, arg01);
    var v0 : List<Int> = mutableListOf(1, 2, 1);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
