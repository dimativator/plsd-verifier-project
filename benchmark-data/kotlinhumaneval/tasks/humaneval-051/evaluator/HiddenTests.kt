fun main() {
    var arg10: String = "abcd"
    var arg11: String = "dddddddabc"
    var x1: Boolean = sameChars(arg10, arg11)
    var v1: Boolean = true
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "dddddddabc"
    var arg21: String = "abcd"
    var x2: Boolean = sameChars(arg20, arg21)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "eabcd"
    var arg31: String = "dddddddabc"
    var x3: Boolean = sameChars(arg30, arg31)
    var v3: Boolean = false
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "abcd"
    var arg41: String = "dddddddabcf"
    var x4: Boolean = sameChars(arg40, arg41)
    var v4: Boolean = false
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "eabcdzzzz"
    var arg51: String = "dddzzzzzzzddddabc"
    var x5: Boolean = sameChars(arg50, arg51)
    var v5: Boolean = false
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "aabb"
    var arg61: String = "aaccc"
    var x6: Boolean = sameChars(arg60, arg61)
    var v6: Boolean = false
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

