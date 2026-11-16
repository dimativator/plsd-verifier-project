fun main() {
    var arg00: String = "abcde"
    var x0: Int = vowelsCount(arg00)
    var v0: Int = 2
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "Alone"
    var x1: Int = vowelsCount(arg10)
    var v1: Int = 3
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "key"
    var x2: Int = vowelsCount(arg20)
    var v2: Int = 2
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "bye"
    var x3: Int = vowelsCount(arg30)
    var v3: Int = 1
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "keY"
    var x4: Int = vowelsCount(arg40)
    var v4: Int = 2
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "bYe"
    var x5: Int = vowelsCount(arg50)
    var v5: Int = 1
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "ACEDY"
    var x6: Int = vowelsCount(arg60)
    var v6: Int = 3
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

