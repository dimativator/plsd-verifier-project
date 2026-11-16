fun main() {
    var arg00 : Int = 2
    var arg01 : Int = 10
    var x0 : List<Int> = generateIntegers(arg00, arg01);
    var v0 : List<Int> = mutableListOf(2, 4, 6, 8);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
