fun main() {
    var arg10: List<Int> = mutableListOf(1, 2, 3, 4)
    var x1: List<Int> = removeDuplicates(arg10)
    var v1: List<Int> = mutableListOf(1, 2, 3, 4)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(1, 2, 3, 2, 4, 3, 5)
    var x2: List<Int> = removeDuplicates(arg20)
    var v2: List<Int> = mutableListOf(1, 4, 5)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

