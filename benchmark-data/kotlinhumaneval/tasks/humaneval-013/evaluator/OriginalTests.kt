fun main() {
    var arg00: Int = 3
    var arg01: Int = 7
    var x0: Int = greatestCommonDivisor(arg00, arg01)
    var v0: Int = 1
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 10
    var arg11: Int = 15
    var x1: Int = greatestCommonDivisor(arg10, arg11)
    var v1: Int = 5
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 49
    var arg21: Int = 14
    var x2: Int = greatestCommonDivisor(arg20, arg21)
    var v2: Int = 7
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 144
    var arg31: Int = 60
    var x3: Int = greatestCommonDivisor(arg30, arg31)
    var v3: Int = 12
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

