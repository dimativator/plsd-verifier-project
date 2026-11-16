fun main() {
    var arg00: Int = 1
    var x0: Int = primeFib(arg00)
    var v0: Int = 2
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 2
    var x1: Int = primeFib(arg10)
    var v1: Int = 3
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 3
    var x2: Int = primeFib(arg20)
    var v2: Int = 5
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 4
    var x3: Int = primeFib(arg30)
    var v3: Int = 13
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 5
    var x4: Int = primeFib(arg40)
    var v4: Int = 89
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 6
    var x5: Int = primeFib(arg50)
    var v5: Int = 233
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 7
    var x6: Int = primeFib(arg60)
    var v6: Int = 1597
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 8
    var x7: Int = primeFib(arg70)
    var v7: Int = 28657
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: Int = 9
    var x8: Int = primeFib(arg80)
    var v8: Int = 514229
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: Int = 10
    var x9: Int = primeFib(arg90)
    var v9: Int = 433494437
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }


}

