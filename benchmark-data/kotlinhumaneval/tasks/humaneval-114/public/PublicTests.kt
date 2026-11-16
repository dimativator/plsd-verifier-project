fun main() {
    var arg00 : String = "Mary had a little lamb"
    var arg01 : Int = 4
    var x0 : List<Any> = selectWords(arg00, arg01);
    var v0 : List<Any> = mutableListOf("little");
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
