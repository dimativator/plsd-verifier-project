fun main() {
    var arg10: Int = 3
    var x1: Int = carRaceCollision(arg10)
    var v1: Int = 9
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 4
    var x2: Int = carRaceCollision(arg20)
    var v2: Int = 16
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 8
    var x3: Int = carRaceCollision(arg30)
    var v3: Int = 64
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 10
    var x4: Int = carRaceCollision(arg40)
    var v4: Int = 100
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

