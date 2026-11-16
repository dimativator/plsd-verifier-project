fun main() {
    var arg10: String = "1077E"
    var x1: Int = hexKey(arg10)
    var v1: Int = 2
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "ABED1A33"
    var x2: Int = hexKey(arg20)
    var v2: Int = 4
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "2020"
    var x3: Int = hexKey(arg30)
    var v3: Int = 2
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "123456789ABCDEF0"
    var x4: Int = hexKey(arg40)
    var v4: Int = 6
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "112233445566778899AABBCCDDEEFF00"
    var x5: Int = hexKey(arg50)
    var v5: Int = 12
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = ""
    var x6: Int = hexKey(arg60)
    var v6: Int = 0
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

