fun main() {
    var arg10: Int = 150
    var x1: String = solve(arg10)
    var v1: String = "110"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 147
    var x2: String = solve(arg20)
    var v2: String = "1100"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 333
    var x3: String = solve(arg30)
    var v3: String = "1001"
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 963
    var x4: String = solve(arg40)
    var v4: String = "10010"
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

