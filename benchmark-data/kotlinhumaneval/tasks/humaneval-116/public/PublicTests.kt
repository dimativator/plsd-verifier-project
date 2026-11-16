fun main() {
    var arg00 : List<String> = mutableListOf("()(", ")")
    var x0 : String = matchParens(arg00);
    var v0 : String = "Yes";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
