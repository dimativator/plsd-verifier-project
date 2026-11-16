fun main() {
    var arg00: String = ""
    var arg01: String = "x"
    var x0: Int = howManyTimes(arg00, arg01)
    var v0: Int = 0
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "xyxyxyx"
    var arg11: String = "x"
    var x1: Int = howManyTimes(arg10, arg11)
    var v1: Int = 4
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "cacacacac"
    var arg21: String = "cac"
    var x2: Int = howManyTimes(arg20, arg21)
    var v2: Int = 4
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "john doe"
    var arg31: String = "john"
    var x3: Int = howManyTimes(arg30, arg31)
    var v3: Int = 1
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

