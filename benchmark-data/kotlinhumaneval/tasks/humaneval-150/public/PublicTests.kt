fun main() {
    var arg00 : String = "Watashi"
    var arg01 : List<String> = mutableListOf("tEN", "niNE", "eIGHt8OKe")
    var x0 : String = strongestExtension(arg00, arg01);
    var v0 : String = "Watashi.eIGHt8OKe";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
