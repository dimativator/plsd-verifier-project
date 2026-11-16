fun main() {
    var arg00 : Int = 3
    var x0 : List<Int> = tri(arg00);
    var v0 : List<Int> = mutableListOf(1, 3, 2, 8);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
