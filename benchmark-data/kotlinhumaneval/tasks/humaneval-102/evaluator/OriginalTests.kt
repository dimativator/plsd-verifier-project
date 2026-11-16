fun main() {
    var arg00: List<Int> = mutableListOf(2, 1, 1, 4, 5, 8, 2, 3)
    var x0: List<String> = byLength(arg00)
    var v0: List<String> = mutableListOf("Eight", "Five", "Four", "Three", "Two", "Two", "One", "One")
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf()
    var x1: List<String> = byLength(arg10)
    var v1: List<String> = mutableListOf()
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(1, -1, 55)
    var x2: List<String> = byLength(arg20)
    var v2: List<String> = mutableListOf("One")
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(1, -1, 3, 2)
    var x3: List<String> = byLength(arg30)
    var v3: List<String> = mutableListOf("Three", "Two", "One")
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(9, 4, 8)
    var x4: List<String> = byLength(arg40)
    var v4: List<String> = mutableListOf("Nine", "Eight", "Four")
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

