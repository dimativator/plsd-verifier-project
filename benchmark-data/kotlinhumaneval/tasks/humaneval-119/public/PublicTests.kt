fun main() {
    var arg00 : List<Int> = mutableListOf(1, -2, -3, 41, 57, 76, 87, 88, 99)
    var arg01 : Int = 3
    var x0 : Int = addElements(arg00, arg01);
    var v0 : Int = -4;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
