fun main() {
    var arg10: List<Int> = mutableListOf(-10, 4, 6, 1000, 10, 20)
    var x1: Double = median(arg10)
    var v1: Double = 8.0
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(5)
    var x2: Double = median(arg20)
    var v2: Double = 5.0
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(6, 5)
    var x3: Double = median(arg30)
    var v3: Double = 5.5
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(8, 1, 3, 9, 9, 2, 7)
    var x4: Double = median(arg40)
    var v4: Double = 7.0
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

