fun main() {
    var arg00 : List<Int> = mutableListOf(1, 2)
    var arg01 : List<Int> = mutableListOf(2, 3)
    var x0 : String = intersection(arg00, arg01);
    var v0 : String = "NO";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
