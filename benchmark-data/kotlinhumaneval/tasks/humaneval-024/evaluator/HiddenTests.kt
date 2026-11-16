fun main() {
    var arg10: Int = 7
    var x1: Int = largestDivisor(arg10)
    var v1: Int = 1
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 10
    var x2: Int = largestDivisor(arg20)
    var v2: Int = 5
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 100
    var x3: Int = largestDivisor(arg30)
    var v3: Int = 50
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 49
    var x4: Int = largestDivisor(arg40)
    var v4: Int = 7
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

