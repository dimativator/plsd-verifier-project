fun main() {
    var arg10: String = "asdfgh"
    var x1: List<Any> = allPrefixes(arg10)
    var v1: List<Any> = mutableListOf("a", "as", "asd", "asdf", "asdfg", "asdfgh")
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "WWW"
    var x2: List<Any> = allPrefixes(arg20)
    var v2: List<Any> = mutableListOf("W", "WW", "WWW")
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

