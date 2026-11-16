fun main() {
    var arg00: Int = 1
    var x0: Int = sumToN(arg00)
    var v0: Int = 1
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 6
    var x1: Int = sumToN(arg10)
    var v1: Int = 21
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 11
    var x2: Int = sumToN(arg20)
    var v2: Int = 66
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 30
    var x3: Int = sumToN(arg30)
    var v3: Int = 465
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 100
    var x4: Int = sumToN(arg40)
    var v4: Int = 5050
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

