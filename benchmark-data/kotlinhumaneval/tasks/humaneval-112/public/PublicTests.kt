fun main() {
    var arg00 : List<List<Int>> = mutableListOf(mutableListOf(0, 0, 1, 0), mutableListOf(0, 1, 0, 0), mutableListOf(1, 1, 1, 1))
    var arg01 : Int = 1
    var x0 : Int = maxFill(arg00, arg01);
    var v0 : Int = 6;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
