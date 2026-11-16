fun main() {
    var arg00: String = ""
    var x0: String = removeVowels(arg00)
    var v0: String = ""
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "abcdef\nghijklm"
    var x1: String = removeVowels(arg10)
    var v1: String = "bcdf\nghjklm"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "fedcba"
    var x2: String = removeVowels(arg20)
    var v2: String = "fdcb"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "eeeee"
    var x3: String = removeVowels(arg30)
    var v3: String = ""
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "acBAA"
    var x4: String = removeVowels(arg40)
    var v4: String = "cB"
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "EcBOO"
    var x5: String = removeVowels(arg50)
    var v5: String = "cB"
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "ybcd"
    var x6: String = removeVowels(arg60)
    var v6: String = "ybcd"
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

