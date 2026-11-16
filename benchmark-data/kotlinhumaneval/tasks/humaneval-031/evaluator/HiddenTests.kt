fun main() {
    var arg10: Int = 101
    var x1: Boolean = isPrime(arg10)
    var v1: Boolean = true
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 11
    var x2: Boolean = isPrime(arg20)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 13441
    var x3: Boolean = isPrime(arg30)
    var v3: Boolean = true
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 61
    var x4: Boolean = isPrime(arg40)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 4
    var x5: Boolean = isPrime(arg50)
    var v5: Boolean = false
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 1
    var x6: Boolean = isPrime(arg60)
    var v6: Boolean = false
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 5
    var x7: Boolean = isPrime(arg70)
    var v7: Boolean = true
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: Int = 11
    var x8: Boolean = isPrime(arg80)
    var v8: Boolean = true
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: Int = 17
    var x9: Boolean = isPrime(arg90)
    var v9: Boolean = true
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100: Int = 85
    var x10: Boolean = isPrime(arg100)
    var v10: Boolean = false
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110: Int = 77
    var x11: Boolean = isPrime(arg110)
    var v11: Boolean = false
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120: Int = 255379
    var x12: Boolean = isPrime(arg120)
    var v12: Boolean = false
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }


}

