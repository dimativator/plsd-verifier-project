fun main() {
    var arg10: Int = 78
    var x1: Int = fizzBuzz(arg10)
    var v1: Int = 2
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 79
    var x2: Int = fizzBuzz(arg20)
    var v2: Int = 3
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 100
    var x3: Int = fizzBuzz(arg30)
    var v3: Int = 3
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 200
    var x4: Int = fizzBuzz(arg40)
    var v4: Int = 6
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 4000
    var x5: Int = fizzBuzz(arg50)
    var v5: Int = 192
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 10000
    var x6: Int = fizzBuzz(arg60)
    var v6: Int = 639
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 100000
    var x7: Int = fizzBuzz(arg70)
    var v7: Int = 8026
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

