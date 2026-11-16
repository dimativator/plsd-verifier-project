fun main() {
    var arg00: Int = 0
    var x0: String = decimalToBinary(arg00)
    var v0: String = "db0db"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 32
    var x1: String = decimalToBinary(arg10)
    var v1: String = "db100000db"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 103
    var x2: String = decimalToBinary(arg20)
    var v2: String = "db1100111db"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 15
    var x3: String = decimalToBinary(arg30)
    var v3: String = "db1111db"
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

