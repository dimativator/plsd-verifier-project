fun main() {
    var arg10: String = "aba"
    var x1: Boolean = isPalindrome(arg10)
    var v1: Boolean = true
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "aaaaa"
    var x2: Boolean = isPalindrome(arg20)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "zbcd"
    var x3: Boolean = isPalindrome(arg30)
    var v3: Boolean = false
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "xywyx"
    var x4: Boolean = isPalindrome(arg40)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "xywyz"
    var x5: Boolean = isPalindrome(arg50)
    var v5: Boolean = false
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "xywzx"
    var x6: Boolean = isPalindrome(arg60)
    var v6: Boolean = false
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

