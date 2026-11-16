fun main() {
    var arg10: List<Int> = mutableListOf(1, 2, 3)
    var x1: List<Int> = derivative(arg10)
    var v1: List<Int> = mutableListOf(2, 6)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(3, 2, 1)
    var x2: List<Int> = derivative(arg20)
    var v2: List<Int> = mutableListOf(2, 2)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(3, 2, 1, 0, 4)
    var x3: List<Int> = derivative(arg30)
    var v3: List<Int> = mutableListOf(2, 2, 0, 16)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(1)
    var x4: List<Int> = derivative(arg40)
    var v4: List<Int> = mutableListOf()
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

