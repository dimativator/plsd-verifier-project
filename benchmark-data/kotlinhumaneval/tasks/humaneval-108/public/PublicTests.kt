fun main() {
    var arg00 : String = "a b b a"
    var x0 : Map<String, Int> = histogram(arg00);
    var v0 : Map<String, Int> = mutableMapOf("a" to 2, "b" to 2);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
