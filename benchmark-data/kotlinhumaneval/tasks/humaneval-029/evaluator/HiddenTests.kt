fun main() {
    var arg10: List<String> = mutableListOf("xxx", "asd", "xxy", "john doe", "xxxAAA", "xxx")
    var arg11: String = "xxx"
    var x1: List<String> = filterByPrefix(arg10, arg11)
    var v1: List<String> = mutableListOf("xxx", "xxxAAA", "xxx")
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }


}

