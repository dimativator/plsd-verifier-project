fun main() {
    var arg00 : String = "Hello world!"
    var x0 : Any = splitWords(arg00);
    var v0 : Any = mutableListOf("Hello", "world!");
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
