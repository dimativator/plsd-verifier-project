fun main() {
    var arg00: List<Int> = mutableListOf()
    var x0: List<Int> = sumProduct(arg00)
    var v0: List<Int> = mutableListOf(0, 1)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(1, 1, 1)
    var x1: List<Int> = sumProduct(arg10)
    var v1: List<Int> = mutableListOf(3, 1)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(100, 0)
    var x2: List<Int> = sumProduct(arg20)
    var v2: List<Int> = mutableListOf(100, 0)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(3, 5, 7)
    var x3: List<Int> = sumProduct(arg30)
    var v3: List<Int> = mutableListOf(15, 105)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(10)
    var x4: List<Int> = sumProduct(arg40)
    var v4: List<Int> = mutableListOf(10, 10)
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

