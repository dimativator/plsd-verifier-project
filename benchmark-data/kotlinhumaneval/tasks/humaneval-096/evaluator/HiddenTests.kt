fun main() {
    var arg10: String = "14.5"
    var x1: Int = closestInteger(arg10)
    var v1: Int = 15
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "-15.5"
    var x2: Int = closestInteger(arg20)
    var v2: Int = -16
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "15.3"
    var x3: Int = closestInteger(arg30)
    var v3: Int = 15
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "0"
    var x4: Int = closestInteger(arg40)
    var v4: Int = 0
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

