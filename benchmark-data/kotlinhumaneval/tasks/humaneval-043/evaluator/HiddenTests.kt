fun main() {
    var arg10: Int = 2
    var arg11: Int = 2
    var x1: Double = triangleArea(arg10, arg11)
    var v1: Double = 2.0
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 10
    var arg21: Int = 8
    var x2: Double = triangleArea(arg20, arg21)
    var v2: Double = 40.0
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

