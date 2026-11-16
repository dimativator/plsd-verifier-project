fun main() {
    var arg00: List<String> = mutableListOf()
    var arg01: String = "john"
    var x0: List<String> = filterByPrefix(arg00, arg01)
    var v0: List<String> = mutableListOf()
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<String> = mutableListOf("xxx", "asd", "xxy", "john doe", "xxxAAA", "xxx")
    var arg11: String = "xxx"
    var x1: List<String> = filterByPrefix(arg10, arg11)
    var v1: List<String> = mutableListOf("xxx", "xxxAAA", "xxx")
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }


}

