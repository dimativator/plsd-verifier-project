fun main() {
    var arg00 : Int = 5
    var arg01 : Int = 6
    var arg02 : Int = 10
    var x0 : List<Int> = eat(arg00, arg01, arg02);
    var v0 : List<Int> = mutableListOf(11, 4);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
