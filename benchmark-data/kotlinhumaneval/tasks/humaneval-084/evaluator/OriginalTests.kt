fun main() {
    var arg00: List<List<Int>> = mutableListOf()
    var arg01: Int = 1
    var x0: List<List<Int>> = getRow(arg00, arg01)
    var v0: List<List<Int>> = mutableListOf()
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<List<Int>> = mutableListOf(mutableListOf(1))
    var arg11: Int = 2
    var x1: List<List<Int>> = getRow(arg10, arg11)
    var v1: List<List<Int>> = mutableListOf()
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<List<Int>> = mutableListOf(mutableListOf(), mutableListOf(1), mutableListOf(1, 2, 3))
    var arg21: Int = 3
    var x2: List<List<Int>> = getRow(arg20, arg21)
    var v2: List<List<Int>> = mutableListOf(mutableListOf(2, 2))
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

