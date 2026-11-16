fun main() {
    var arg00: String = "(()()) ((())) () ((())()())"
    var x0: List<Int> = parseNestedParens(arg00)
    var v0: List<Int> = mutableListOf(2, 3, 1, 3)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

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

