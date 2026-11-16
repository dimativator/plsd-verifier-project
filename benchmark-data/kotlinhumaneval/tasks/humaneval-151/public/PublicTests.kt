fun main() {
    var arg00 : String = "xyzw"
    var arg01 : String = "xyw"
    var x0 : Boolean = cycpatternCheck(arg00, arg01);
    var v0 : Boolean = false;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
