fun main() {
    var arg00: String = "(()()) ((())) () ((())()())"
    var x0: List<Int> = parseNestedParens(arg00)
    var v0: List<Int> = mutableListOf(2, 3, 1, 3)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
