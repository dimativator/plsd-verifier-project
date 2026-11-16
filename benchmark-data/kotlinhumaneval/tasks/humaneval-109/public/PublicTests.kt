fun main() {
    var arg00 : String = "abcde"
    var arg01 : String = "ae"
    var x0 : Pair<String, Boolean> = reverseDelete(arg00, arg01);
    var v0 : Pair<String, Boolean> = Pair("bcd", false)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
