fun main() {
    var arg00: String = ""
    var x0: String = makePalindrome(arg00)
    var v0: String = ""
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "x"
    var x1: String = makePalindrome(arg10)
    var v1: String = "x"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "xyz"
    var x2: String = makePalindrome(arg20)
    var v2: String = "xyzyx"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "xyx"
    var x3: String = makePalindrome(arg30)
    var v3: String = "xyx"
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "jerry"
    var x4: String = makePalindrome(arg40)
    var v4: String = "jerryrrej"
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

