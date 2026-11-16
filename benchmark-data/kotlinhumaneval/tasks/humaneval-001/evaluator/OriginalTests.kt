fun main() {
    var arg00: String = "(()()) ((())) () ((())()())"
    var x0: List<String> = separateParenGroups(arg00)
    var v0: List<String> = mutableListOf("(()())", "((()))", "()", "((())()())")
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "() (()) ((())) (((())))"
    var x1: List<String> = separateParenGroups(arg10)
    var v1: List<String> = mutableListOf("()", "(())", "((()))", "(((())))")
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "(()(())((())))"
    var x2: List<String> = separateParenGroups(arg20)
    var v2: List<String> = mutableListOf("(()(())((())))")
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "( ) (( )) (( )( ))"
    var x3: List<String> = separateParenGroups(arg30)
    var v3: List<String> = mutableListOf("()", "(())", "(()())")
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

