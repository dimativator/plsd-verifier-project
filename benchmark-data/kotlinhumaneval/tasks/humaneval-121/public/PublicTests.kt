fun main() {
    var arg00 : String = "03-11-2000"
    var x0 : Boolean = validDate(arg00);
    var v0 : Boolean = true;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
