fun main() {
    var arg00: String = ""
    var x0: Int = digitsum(arg00)
    var v0: Int = 0
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "abAB"
    var x1: Int = digitsum(arg10)
    var v1: Int = 131
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "abcCd"
    var x2: Int = digitsum(arg20)
    var v2: Int = 67
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "helloE"
    var x3: Int = digitsum(arg30)
    var v3: Int = 69
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "woArBld"
    var x4: Int = digitsum(arg40)
    var v4: Int = 131
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "aAaaaXa"
    var x5: Int = digitsum(arg50)
    var v5: Int = 153
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = " How are yOu?"
    var x6: Int = digitsum(arg60)
    var v6: Int = 151
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: String = "You arE Very Smart"
    var x7: Int = digitsum(arg70)
    var v7: Int = 327
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

