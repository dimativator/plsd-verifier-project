fun main() {
    var arg10: String = "() (()) ((())) (((())))"
    var x1: List<Int> = parseNestedParens(arg10)
    var v1: List<Int> = mutableListOf(1, 2, 3, 4)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "(()(())((())))"
    var x2: List<Int> = parseNestedParens(arg20)
    var v2: List<Int> = mutableListOf(4)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

