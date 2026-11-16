fun main() {
    var arg10: Int = 27
    var x1: Int = largestPrimeFactor(arg10)
    var v1: Int = 3
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 63
    var x2: Int = largestPrimeFactor(arg20)
    var v2: Int = 7
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 330
    var x3: Int = largestPrimeFactor(arg30)
    var v3: Int = 11
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 13195
    var x4: Int = largestPrimeFactor(arg40)
    var v4: Int = 29
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

