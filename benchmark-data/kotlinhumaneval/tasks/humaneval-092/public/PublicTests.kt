fun main() {
    var arg00: Map<Any?, Any?> = mutableMapOf("p" to "pineapple", "b" to "banana")
    var x0: Boolean = checkDictCase(arg00)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
