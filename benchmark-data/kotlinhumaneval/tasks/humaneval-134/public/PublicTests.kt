fun main() {
    var arg00 : Any = 1
    var arg01 : Any = 2
    var x0 : Any? = compareOne(arg00, arg01);
    var v0 : Any? = 2;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
