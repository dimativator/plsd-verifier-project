fun main() {
    var arg10: List<Any> = mutableListOf(4, mutableMapOf<Any, Any>(), mutableListOf<Any>(), 23.2, 9, "adasd")
    var x1: List<Any> = filterIntegers(arg10)
    var v1: List<Any> = mutableListOf(4, 9)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Any> = mutableListOf(3, "c", 3, 3, "a", "b")
    var x2: List<Any> = filterIntegers(arg20)
    var v2: List<Any> = mutableListOf(3, 3, 3)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

