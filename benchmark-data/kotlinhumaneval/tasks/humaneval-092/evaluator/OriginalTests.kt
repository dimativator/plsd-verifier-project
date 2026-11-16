fun main() {
    var arg00: Map<Any?, Any?> = mutableMapOf("p" to "pineapple", "b" to "banana")
    var x0: Boolean = checkDictCase(arg00)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Map<Any?, Any?> = mutableMapOf("p" to "pineapple", "A" to "banana", "B" to "banana")
    var x1: Boolean = checkDictCase(arg10)
    var v1: Boolean = false
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Map<Any?, Any?> = mutableMapOf("p" to "pineapple", 5 to "banana", "a" to "apple")
    var x2: Boolean = checkDictCase(arg20)
    var v2: Boolean = false
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Map<Any?, Any?> = mutableMapOf("Name" to "John", "Age" to "36", "City" to "Houston")
    var x3: Boolean = checkDictCase(arg30)
    var v3: Boolean = false
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Map<Any?, Any?> = mutableMapOf("STATE" to "NC", "ZIP" to "12345")
    var x4: Boolean = checkDictCase(arg40)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Map<Any?, Any?> = mutableMapOf("fruit" to "Orange", "taste" to "Sweet")
    var x5: Boolean = checkDictCase(arg50)
    var v5: Boolean = true
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Map<Any?, Any?> = mutableMapOf()
    var x6: Boolean = checkDictCase(arg60)
    var v6: Boolean = false
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

