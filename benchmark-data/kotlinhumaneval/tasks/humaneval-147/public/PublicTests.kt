fun main() {
    var arg00 : Int = 7
    var arg01 : Int = 34
    var arg02 : Int = 12
    var x0 : Int = xOrY(arg00, arg01, arg02);
    var v0 : Int = 34;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
