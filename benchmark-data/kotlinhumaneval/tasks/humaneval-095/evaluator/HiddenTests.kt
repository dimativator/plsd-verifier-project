fun main() {
    var arg10: String = "dBBE"
    var x1: Int = countUpper(arg10)
    var v1: Int = 0
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = ""
    var x2: Int = countUpper(arg20)
    var v2: Int = 0
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "EEEE"
    var x3: Int = countUpper(arg30)
    var v3: Int = 2
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

