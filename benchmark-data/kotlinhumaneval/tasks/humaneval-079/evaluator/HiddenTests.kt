fun main() {
    var arg10: String = "abcdcba"
    var x1: Boolean = primeLength(arg10)
    var v1: Boolean = true
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "kittens"
    var x2: Boolean = primeLength(arg20)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "orange"
    var x3: Boolean = primeLength(arg30)
    var v3: Boolean = false
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "wow"
    var x4: Boolean = primeLength(arg40)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "world"
    var x5: Boolean = primeLength(arg50)
    var v5: Boolean = true
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "MadaM"
    var x6: Boolean = primeLength(arg60)
    var v6: Boolean = true
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: String = "Wow"
    var x7: Boolean = primeLength(arg70)
    var v7: Boolean = true
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: String = ""
    var x8: Boolean = primeLength(arg80)
    var v8: Boolean = false
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: String = "HI"
    var x9: Boolean = primeLength(arg90)
    var v9: Boolean = true
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100: String = "go"
    var x10: Boolean = primeLength(arg100)
    var v10: Boolean = true
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110: String = "gogo"
    var x11: Boolean = primeLength(arg110)
    var v11: Boolean = false
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120: String = "aaaaaaaaaaaaaaa"
    var x12: Boolean = primeLength(arg120)
    var v12: Boolean = false
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }

    var arg130: String = "Madam"
    var x13: Boolean = primeLength(arg130)
    var v13: Boolean = true
    if (x13 != v13) {
        throw Exception("Exception -- test case 13 did not pass. x13 = " + x13)
    }

    var arg140: String = "M"
    var x14: Boolean = primeLength(arg140)
    var v14: Boolean = false
    if (x14 != v14) {
        throw Exception("Exception -- test case 14 did not pass. x14 = " + x14)
    }

    var arg150: String = "0"
    var x15: Boolean = primeLength(arg150)
    var v15: Boolean = false
    if (x15 != v15) {
        throw Exception("Exception -- test case 15 did not pass. x15 = " + x15)
    }


}

