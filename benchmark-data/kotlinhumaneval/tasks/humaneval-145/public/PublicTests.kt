fun main() {
    var arg00 : String = "Jupiter"
    var arg01 : String = "Neptune"
    var x0 : List<String> = bf(arg00, arg01);
    var v0 : List<String> = mutableListOf("Saturn", "Uranus");
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
