fun main() {
    var arg00: List<String> = mutableListOf()
    var x0: String? = longest(arg00)
    var v0: String? = null
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<String> = mutableListOf("x", "y", "z")
    var x1: String? = longest(arg10)
    var v1: String? = "x"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<String> = mutableListOf("x", "yyy", "zzzz", "www", "kkkk", "abc")
    var x2: String? = longest(arg20)
    var v2: String? = "zzzz"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

