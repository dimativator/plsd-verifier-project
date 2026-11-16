fun main() {
    var arg00: List<String> = mutableListOf("**", "*", "+")
    var arg01: List<Int> = mutableListOf(2, 3, 4, 5)
    var x0: Int = doAlgebra(arg00, arg01);
    var v0: Int = 37;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
