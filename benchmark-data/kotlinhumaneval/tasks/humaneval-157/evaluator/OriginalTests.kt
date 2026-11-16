fun main() {
    var arg00: List<String> = mutableListOf("**", "*", "+")
    var arg01: List<Int> = mutableListOf(2, 3, 4, 5)
    var x0: Int = doAlgebra(arg00, arg01);
    var v0: Int = 37;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<String> = mutableListOf("+", "*", "-")
    var arg11: List<Int> = mutableListOf(2, 3, 4, 5)
    var x1: Int = doAlgebra(arg10, arg11);
    var v1: Int = 9;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<String> = mutableListOf("//", "*")
    var arg21: List<Int> = mutableListOf(7, 3, 4)
    var x2: Int = doAlgebra(arg20, arg21);
    var v2: Int = 8;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

