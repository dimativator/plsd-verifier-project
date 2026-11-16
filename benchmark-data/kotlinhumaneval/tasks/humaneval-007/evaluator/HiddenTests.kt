fun main() {
    var arg10: List<String> = mutableListOf("xxx", "asd", "xxy", "john doe", "xxxAAA", "xxx")
    var arg11: String = "xxx"
    var x1: List<String> = filterBySubstring(arg10, arg11)
    var v1: List<String> = mutableListOf("xxx", "xxxAAA", "xxx")
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<String> = mutableListOf("xxx", "asd", "aaaxxy", "john doe", "xxxAAA", "xxx")
    var arg21: String = "xx"
    var x2: List<String> = filterBySubstring(arg20, arg21)
    var v2: List<String> = mutableListOf("xxx", "aaaxxy", "xxxAAA", "xxx")
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<String> = mutableListOf("grunt", "trumpet", "prune", "gruesome")
    var arg31: String = "run"
    var x3: List<String> = filterBySubstring(arg30, arg31)
    var v3: List<String> = mutableListOf("grunt", "prune")
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

