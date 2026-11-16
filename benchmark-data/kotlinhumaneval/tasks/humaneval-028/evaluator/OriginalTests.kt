fun main() {
    var arg00: List<String> = mutableListOf()
    var x0: String = concatenate(arg00)
    var v0: String = ""
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<String> = mutableListOf("x", "y", "z")
    var x1: String = concatenate(arg10)
    var v1: String = "xyz"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<String> = mutableListOf("x", "y", "z", "w", "k")
    var x2: String = concatenate(arg20)
    var v2: String = "xyzwk"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

