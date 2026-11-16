fun main() {
    var arg00 : String = "Example"
    var x0 : String = fixSpaces(arg00);
    var v0 : String = "Example";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
