fun main() {
    var arg10: String = "x"
    var x1: Int = strlen(arg10)
    var v1: Int = 1
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "asdasnakj"
    var x2: Int = strlen(arg20)
    var v2: Int = 9
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

