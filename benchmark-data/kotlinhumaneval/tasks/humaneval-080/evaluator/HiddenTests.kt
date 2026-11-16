fun main() {
    var arg10: Int = 2
    var x1: Int = startsOneEnds(arg10)
    var v1: Int = 18
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 3
    var x2: Int = startsOneEnds(arg20)
    var v2: Int = 180
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 4
    var x3: Int = startsOneEnds(arg30)
    var v3: Int = 1800
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 5
    var x4: Int = startsOneEnds(arg40)
    var v4: Int = 18000
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

