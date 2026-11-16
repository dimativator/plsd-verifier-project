fun main() {
    var arg00 : String = "Hello world"
    var x0 : String? = stringToMd5(arg00);
    var v0 : String? = "3e25960a79dbc69b674cd4ec67a72c62";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
