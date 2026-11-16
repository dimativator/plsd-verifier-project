fun main() {
    var arg00 : String = "1/5"
    var arg01 : String = "5/1"
    var x0 : Boolean = simplify(arg00, arg01);
    var v0 : Boolean = true;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
