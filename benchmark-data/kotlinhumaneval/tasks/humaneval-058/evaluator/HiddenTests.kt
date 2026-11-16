fun main() {
    var arg10: String = "(()())"
    var x1: Boolean = correctBracketing2(arg10)
    var v1: Boolean = true
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "()()(()())()"
    var x2: Boolean = correctBracketing2(arg20)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "()()((()()())())(()()(()))"
    var x3: Boolean = correctBracketing2(arg30)
    var v3: Boolean = true
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "((()())))"
    var x4: Boolean = correctBracketing2(arg40)
    var v4: Boolean = false
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = ")(()"
    var x5: Boolean = correctBracketing2(arg50)
    var v5: Boolean = false
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "("
    var x6: Boolean = correctBracketing2(arg60)
    var v6: Boolean = false
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: String = "(((("
    var x7: Boolean = correctBracketing2(arg70)
    var v7: Boolean = false
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: String = ")"
    var x8: Boolean = correctBracketing2(arg80)
    var v8: Boolean = false
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: String = "(()"
    var x9: Boolean = correctBracketing2(arg90)
    var v9: Boolean = false
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100: String = "()()(()())())(()"
    var x10: Boolean = correctBracketing2(arg100)
    var v10: Boolean = false
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110: String = "()()(()())()))()"
    var x11: Boolean = correctBracketing2(arg110)
    var v11: Boolean = false
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }


}

