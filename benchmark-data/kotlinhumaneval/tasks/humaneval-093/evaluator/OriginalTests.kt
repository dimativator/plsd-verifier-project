fun main() {
    var arg00: Int = 5
    var x0: List<Any> = countUpTo(arg00)
    var v0: List<Any> = mutableListOf(2, 3)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 6
    var x1: List<Any> = countUpTo(arg10)
    var v1: List<Any> = mutableListOf(2, 3, 5)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 7
    var x2: List<Any> = countUpTo(arg20)
    var v2: List<Any> = mutableListOf(2, 3, 5)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 10
    var x3: List<Any> = countUpTo(arg30)
    var v3: List<Any> = mutableListOf(2, 3, 5, 7)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 0
    var x4: List<Any> = countUpTo(arg40)
    var v4: List<Any> = mutableListOf()
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 22
    var x5: List<Any> = countUpTo(arg50)
    var v5: List<Any> = mutableListOf(2, 3, 5, 7, 11, 13, 17, 19)
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 1
    var x6: List<Any> = countUpTo(arg60)
    var v6: List<Any> = mutableListOf()
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 18
    var x7: List<Any> = countUpTo(arg70)
    var v7: List<Any> = mutableListOf(2, 3, 5, 7, 11, 13, 17)
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: Int = 47
    var x8: List<Any> = countUpTo(arg80)
    var v8: List<Any> = mutableListOf(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: Int = 101
    var x9: List<Any> = countUpTo(arg90)
    var v9: List<Any> =
        mutableListOf(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }


}

