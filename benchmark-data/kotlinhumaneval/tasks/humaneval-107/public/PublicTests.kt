fun main() {
    var arg00 : List<Int> = mutableListOf(1, 2, 3, 4)
    var arg01 : List<Int> = mutableListOf(1, 2, 3, 4)
    var x0 : String = exchange(arg00, arg01);
    var v0 : String = "YES";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
