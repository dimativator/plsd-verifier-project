fun main() {
    var arg00: String = "(()()) ((())) () ((())()())"
    var x0: List<String> = separateParenGroups(arg00)
    var v0: List<String> = mutableListOf("(()())", "((()))", "()", "((())()())")
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
