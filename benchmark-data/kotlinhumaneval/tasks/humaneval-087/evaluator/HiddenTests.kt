fun main() {
    var arg10: List<Int> = mutableListOf(5, 1, 4, 3, 2)
    var x1: Int? = nextSmallest(arg10)
    var v1: Int? = 2
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf()
    var x2: Int? = nextSmallest(arg20)
    var v2: Int? = null
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(1, 1)
    var x3: Int? = nextSmallest(arg30)
    var v3: Int? = null
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(1, 1, 1, 1, 0)
    var x4: Int? = nextSmallest(arg40)
    var v4: Int? = 1
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(1, 1)
    var x5: Int? = nextSmallest(arg50)
    var v5: Int? = null
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(-35, 34, 12, -45)
    var x6: Int? = nextSmallest(arg60)
    var v6: Int? = -35
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

