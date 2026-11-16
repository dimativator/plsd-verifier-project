fun main() {
    var arg00 : Int = 5
    var x0 : List<Int> = f(arg00);
    var v0 : List<Int> = mutableListOf(1, 2, 6, 24, 15);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
